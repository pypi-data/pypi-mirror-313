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
import base64
import datetime
import json
from typing import Any, Optional, Union

from mlflow.models.model import ModelInfo

from runway.model_registry.values import ModelFramework


# NOTE refer to following links:
# https://github.com/mlflow/mlflow/blob/672391a4375cedf554e4c11fd3bc8213492f242f/dev/set_matrix.py#L502
# https://github.com/mlflow/mlflow/blob/8695eddd320f7a2ac60d3644acc2fd82548cbdb0/mlflow/utils/proto_json_utils.py#L160
class CustomEncoder(json.JSONEncoder):
    def try_convert(self, o: Any) -> Any:
        import numpy as np
        import pandas as pd
        from mlflow.types.utils import DataType

        def encode_binary(x: Any) -> str:
            return base64.encodebytes(x).decode("ascii")

        if isinstance(o, np.ndarray):
            if o.dtype == object:
                return [self.try_convert(x)[0] for x in o.tolist()], True
            elif o.dtype == np.bytes_:
                return np.vectorize(encode_binary)(o), True
            else:
                return o.tolist(), True
        if isinstance(o, np.generic):
            return o.item(), True
        if isinstance(o, (bytes, bytearray)):
            return encode_binary(o), True
        if isinstance(o, np.datetime64):
            return np.datetime_as_string(o), True
        if isinstance(
            o,
            (pd.Timestamp, datetime.date, datetime.datetime, datetime.time),
        ):
            return o.isoformat(), True
        if isinstance(o, (DataType)):
            return o.to_numpy().name, True

        return o, False

    def default(self, o: Any) -> Any:
        res, converted = self.try_convert(o)
        if converted:
            return res
        else:
            return super().default(o)


def stringify_io_name_by_module(
    iotype: str,
    idx: int,
    framework: Union[str, ModelFramework],
    model: Optional[Any] = None,
) -> str:
    if framework in ["xgboost", "pytorch", "sklearn"]:
        return f"{iotype}__{idx}"
    if framework in ["tensorflow"]:
        if model and hasattr(model, "signature") and model.signature:
            return list(model.signature.inputs)[idx].name  # type: ignore
        return model.input_names[idx]  # type: ignore
    return f"{iotype}{idx}"


def extract_model_path_from_mlflow(
    model_info: ModelInfo,
    framework: Union[str, ModelFramework],
) -> str:
    def _get_xgboost_model_path_property(flavors: dict) -> str:
        """
        python_function:
            data: model.bst
            env:
                conda: conda.yaml
                virtualenv: python_env.yaml
            loader_module: mlflow.xgboost
            python_version: 3.9.16
        xgboost:
            code: null
            data: model.bst
            model_class: xgboost.sklearn.XGBClassifier
            model_format: bst
            xgb_version: 1.7.5
        """
        return flavors["xgboost"]["data"]

    def _get_sklearn_model_path_property(flavors: dict) -> str:
        """
        python_function:
            env: conda.yaml
            loader_module: mlflow.sklearn
            model_path: model.pkl
            predict_fn: predict
            python_version: 3.9.15
        sklearn:
            code: null
            pickled_model: model.pkl
            serialization_format: cloudpickle
            sklearn_version: 1.2.2
        """
        return flavors["sklearn"]["pickled_model"]

    def _get_tensorflow_model_path_property(flavors: dict) -> str:
        """
        python_function:
            env: conda.yaml
            loader_module: mlflow.tensorflow
            python_version: 3.9.15
        tensorflow:
            code: null
            meta_graph_tags:
            - serve
            saved_model_dir: tfmodel
            signature_def_key: serving_default
        """
        if "data" in flavors["tensorflow"]:
            return flavors["tensorflow"]["data"] + "/model/saved_model.pb"
        return flavors["tensorflow"]["saved_model_dir"]

    def _get_pytorch_model_path_property(flavors: dict) -> str:
        """
        python_function:
            data: data
            env:
                conda: conda.yaml
                virtualenv: python_env.yaml
            loader_module: mlflow.pytorch
            pickle_module_name: mlflow.pytorch.pickle_module
            python_version: 3.9.16
        pytorch:
            code: null
            model_data: data
            pytorch_version: 2.0.1
        """
        return flavors["pytorch"]["model_data"] + "/model.pth"

    def _get_onnx_model_path_property(flavors: dict) -> str:
        """
        onnx:
            code: null
            data: model.onnx
            onnx_version: 1.14.0
            providers:
            - CUDAExecutionProvider
            - CPUExecutionProvider
        python_function:
            data: model.onnx
            env:
                conda: conda.yaml
                virtualenv: python_env.yaml
            loader_module: mlflow.onnx
            python_version: 3.9.16
        """
        return flavors["python_function"]["data"]

    def _get_pyfunc_model_path_property(flavors: dict) -> str:
        """
        python_function:
            cloudpickle_version: 2.2.1
            env:
            conda: conda.yaml
            virtualenv: python_env.yaml
            loader_module: mlflow.pyfunc.model
            python_model: python_model.pkl
            python_version: 3.9.18
        """
        return flavors["python_function"]["python_model"]

    return {
        "xgboost": _get_xgboost_model_path_property,
        "sklearn": _get_sklearn_model_path_property,
        "tensorflow": _get_tensorflow_model_path_property,
        "pytorch": _get_pytorch_model_path_property,
        "onnx": _get_onnx_model_path_property,
        "pyfunc": _get_pyfunc_model_path_property,
    }[framework](model_info.flavors)
