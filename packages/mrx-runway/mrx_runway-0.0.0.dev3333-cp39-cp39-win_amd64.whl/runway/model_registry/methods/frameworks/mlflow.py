#
#  MAKINAROCKS CONFIDENTIAL
#  ________________________
#
#  [2017] - [2024] MakinaRocks Co., Ltd.
#  All Rights Reserved.
#
#  NOTICE:  All information contained herein is, and remains
#  the property of MakinaRocks Co., Ltd. and its suppliers, if any.
#  The intellectual and technical concepts contained herein are
#  proprietary to MakinaRocks Co., Ltd. and its suppliers and may be
#  covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law. Dissemination
#  of this information or reproduction of this material is
#  strictly forbidden unless prior written permission is obtained
#  from MakinaRocks Co., Ltd.
from pathlib import Path
from typing import Any, Callable, Dict, Final, Optional, Tuple, Union
from urllib.parse import urlparse

import boto3
import mlflow
from mlflow.pyfunc import PyFuncModel
import numpy as np
import pandas as pd
from mlflow.models.model import ModelInfo

from runway.model_registry.methods.common import (
    ModelInputsSample,
    ModelOutputsSample,
    is_supported_primitive_class,
)
from runway.model_registry.values import ModelFramework
from runway.settings import MLFlowModelRegistryData, settings

from ..frameworks.common import has_method_names


def _evaluate_pyfunc_model(
    model: PyFuncModel,
    method_name: str,
    sample: Union[pd.DataFrame, np.ndarray, pd.Series, str, bytes],
) -> ModelOutputsSample:
    # NOTE 실제 구현된 class object 에 접근
    # https://mlflow.org/docs/latest/python_api/mlflow.pyfunc.html#mlflow.pyfunc.PyFuncModel.unwrap_python_model
    unwrapped_model = model.unwrap_python_model()
    has_method_names(unwrapped_model, [method_name])

    return getattr(unwrapped_model, method_name)(
        None,  # TODO 나중에는 load_context() 를 호출하는 로직 구현 필요
        sample.copy() if isinstance(sample, pd.DataFrame) else sample,
    )


def _evaluate_basis_model(
    model: Any,
    method_name: str,
    sample: Union[pd.DataFrame, np.ndarray, pd.Series, str, bytes],
) -> ModelOutputsSample:
    return getattr(model, method_name)(
        sample.copy() if isinstance(sample, pd.DataFrame) else sample,
    )


def _evaluate_onnx_model(
    model: Any,
    method_name: str,
    sample: Union[pd.DataFrame, np.ndarray, pd.Series, str, bytes],
) -> ModelOutputsSample:
    from onnxruntime import backend  # pylint: disable=import-outside-toplevel
    from onnxruntime import get_device  # pylint: disable=import-outside-toplevel

    rep = backend.prepare(model, get_device())
    has_method_names(rep, [method_name])

    return getattr(rep, method_name)(sample)


def _evaluate_pytorch_model(
    model: Any,
    method_name: str,
    sample: Union[pd.DataFrame, np.ndarray, pd.Series, str, bytes],
) -> ModelOutputsSample:
    import torch  # pylint: disable=import-outside-toplevel

    if method_name == "forward":
        output_sample = getattr(model, method_name)(torch.from_numpy(sample))
        return output_sample.detach().numpy()
    else:
        # NOTE forward method 가 아니라 사용자가 임의로 추가한 함수를 따르는 경우는 그대로
        return getattr(model, method_name)(sample)


def _evaluate_tensorflow_model(
    model: Any,
    method_name: str,
    sample: Union[pd.DataFrame, np.ndarray, pd.Series, str, bytes],
) -> ModelOutputsSample:
    return getattr(model, method_name)(sample)[0]


def extract_framework_type_from(model_info: ModelInfo) -> ModelFramework:
    "framework type 을 추출한다."
    if len(model_info.flavors) == 1:
        return ModelFramework.pyfunc
    for framework in EVALUATION_FUNC_MAP:
        if framework in model_info.flavors:
            return framework

    raise RuntimeError(f"not found framework evaluation class: {model_info.flavors=}")


def get_artifact_size_bytes(run: Optional[mlflow.ActiveRun], model_info: ModelInfo) -> int:
    """calculate artifact byte size."""
    if run is None:
        raise ValueError("not found active run")

    if settings.model_registry is None or settings.model_registry.data is None:
        raise ValueError("There are no model registry")

    data = settings.model_registry.data
    url = urlparse(run.info.artifact_uri + "/" + model_info.artifact_path)
    if url.scheme == "s3" and isinstance(data, MLFlowModelRegistryData):
        total_size = 0
        for obj in boto3.client(
            "s3",
            endpoint_url=data.storage_url,
            aws_access_key_id=data.access_key_id,
            aws_secret_access_key=data.secret_access_key,
        ).list_objects_v2(Bucket=url.netloc, Prefix=url.path)["Contents"]:
            total_size += obj["Size"]
        return total_size
    elif url.scheme == "file":
        return sum(f.stat().st_size for f in Path(url.path).glob("**/*") if f.is_file())

    raise ValueError(f"unsupported url schema: {run.info.artifact_uri=}")


def evaluate_model(
    model_info: ModelInfo,
    inputs_sample: ModelInputsSample,
) -> ModelOutputsSample:
    """runtime model verification 작업으로 evaluate (입력 샘플 추론) 를 수행한다."""
    framework = extract_framework_type_from(model_info)
    if framework not in EVALUATION_FUNC_MAP:
        raise ValueError(f"not supported framework({EVALUATION_FUNC_MAP.keys()})")
    if not isinstance(inputs_sample, dict):
        raise ValueError("inputs_sample should be a dictionary")

    lazy_verifying_method_names, evaluate_fn, load_fn = EVALUATION_FUNC_MAP[framework]
    model = load_fn(model_info.model_uri)
    if not lazy_verifying_method_names:
        has_method_names(model, list(inputs_sample.keys()))

    outputs_sample = {}
    for method_name, input_sample in inputs_sample.items():
        method_sample = []
        for sample in input_sample:
            output_sample = evaluate_fn(model, method_name, sample)
            if isinstance(output_sample, list):
                output_sample = np.array(output_sample)
            if not is_supported_primitive_class(output_sample):
                raise ValueError(
                    "unsupported outputs_sample: %s"
                    "supported type must be in "
                    "pd.DataFrame, np.ndarray, pd.Series, str, bytes",
                    type(output_sample),
                )
            method_sample.append(output_sample)
        outputs_sample[method_name] = method_sample

    return outputs_sample


EVALUATION_FUNC_MAP: Final[
    Dict[ModelFramework, Tuple[bool, Callable[..., Any], Callable[..., Any]]]
] = {
    #   (framework): (lazy_verifying_method_names, evaluate_fn, load_fn)
    ModelFramework.onnx: (True, _evaluate_onnx_model, mlflow.onnx.load_model),
    ModelFramework.pytorch: (False, _evaluate_pytorch_model, mlflow.pytorch.load_model),
    ModelFramework.pyfunc: (True, _evaluate_pyfunc_model, mlflow.pyfunc.load_model),
    ModelFramework.sklearn: (False, _evaluate_basis_model, mlflow.sklearn.load_model),
    ModelFramework.tensorflow: (
        False,
        _evaluate_tensorflow_model,
        mlflow.tensorflow.load_model,
    ),
    ModelFramework.xgboost: (False, _evaluate_basis_model, mlflow.xgboost.load_model),
}
