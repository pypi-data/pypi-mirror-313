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
from typing import Any, Dict, List, Optional, Union

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack

import numpy as np
import pandas as pd
from pydantic import BaseModel

from runway.image_snapshot.api_client import ImageSnapshotInfo, create_image_snapshot
from runway.model_registry.schemas import MLFlowEssentialData, WandbEssentialData
from runway.model_registry.values import ModelFramework, ModelRegistryType
from runway.settings import settings

EssentialData = Union[MLFlowEssentialData, WandbEssentialData]
ModelInputsSample = Union[pd.DataFrame, np.ndarray, pd.Series, str, bytes, list, dict]
ModelOutputsSample = dict


def _generate_mlflow_extra_for_image_snapshot(essential: BaseModel) -> dict:
    if settings.model_registry is None:
        raise ValueError("There are no model registry")

    if settings.launch_params is None:
        raise ValueError("There are no launch parameters")

    extra = {"model": essential.dict()}
    if settings.model_registry.id:
        extra["model_registry"] = {
            "id": settings.model_registry.id,
            "data": settings.model_registry.data.dict()
            if settings.model_registry.data is not None
            else {},
        }
    if settings.launch_params.source:
        extra["source"] = settings.launch_params.source.dict()

    return extra


def extract_essential_model_data(
    type: ModelRegistryType, **kwargs: Unpack[Dict[str, Any]]
) -> EssentialData:
    if type == ModelRegistryType.mlflow:
        return MLFlowEssentialData(type=type, **kwargs)
    if type == ModelRegistryType.wandb:
        return WandbEssentialData(type=type, **kwargs)

    raise ValueError(f"unsupported model registry type: {type=}")


def snapshot_container_image(
    essential: EssentialData,
    repository_name: str,
    force: Optional[bool] = None,
    **kwargs: Unpack[Dict[str, Any]],
) -> ImageSnapshotInfo:
    if force is not None and not isinstance(force, bool):
        raise ValueError(f"force parameter must be of type bool, got {type(force)}")

    extra = _generate_mlflow_extra_for_image_snapshot(essential)
    return create_image_snapshot(
        repository_name,
        extra=extra,
        force=force,
        **kwargs,
    )


def is_supported_primitive_class(sample: Any) -> bool:
    return sample.__class__ in [pd.DataFrame, np.ndarray, pd.Series, str, bytes]


def get_inference_method_name(framework: ModelFramework) -> str:
    if framework == ModelFramework.onnx:
        return "run"
    elif framework == ModelFramework.pytorch:
        return "forward"
    elif framework in [
        ModelFramework.pyfunc,
        ModelFramework.sklearn,
        ModelFramework.tensorflow,
        ModelFramework.xgboost,
    ]:
        return "predict"
    else:
        raise ValueError(f"not supported framework: {framework=})")


def fillout_inputs_sample(
    framework: ModelFramework,
    inputs_sample: ModelInputsSample,
) -> dict:
    """non-dictionary inputs_sample 을 최종 형태인 dict[str, list] 로 변환한다."""
    # NOTE 아래서 처리될 list 로 변환해준다.
    method_names: List[str] = []
    method_samples: List[List[ModelInputsSample]] = []
    if is_supported_primitive_class(inputs_sample):
        method_names = [get_inference_method_name(framework)]
        method_samples = [[inputs_sample]]
    elif isinstance(inputs_sample, list):
        method_names = [get_inference_method_name(framework)]
        method_samples = [inputs_sample]
    elif isinstance(inputs_sample, dict):
        method_names = list(inputs_sample.keys())
        method_samples = []
        for _samples in inputs_sample.values():
            method_samples.append(
                _samples if isinstance(_samples, list) else [_samples],
            )
    else:
        raise ValueError(
            "unsupported inputs_sample: "
            "type must be in list, dict"
            "pd.DataFrame, np.ndarray, pd.Series, str, bytes",
        )

    for samples in method_samples:
        if not any(is_supported_primitive_class(sample) for sample in samples):
            raise ValueError(
                "unsupported inputs_sample: "
                "supported type must be in "
                "pd.DataFrame, np.ndarray, pd.Series, str, bytes",
            )

    return {method_names[idx]: samples for idx, samples in enumerate(method_samples)}
