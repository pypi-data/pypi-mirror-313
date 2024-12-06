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

from typing import Any, Dict, Optional

from runway.image_snapshot.api_client import ImageSnapshotInfo

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack

import mlflow
from mlflow.models.model import ModelInfo

from runway.model_registry.methods.artifacts import RunwayModelArtifacts
from runway.model_registry.methods.common import (
    extract_essential_model_data,
    fillout_inputs_sample,
    snapshot_container_image,
)
from runway.model_registry.methods.frameworks.mlflow import (
    ModelInputsSample,
    evaluate_model,
    extract_framework_type_from,
    get_artifact_size_bytes,
)
from runway.model_registry.schemas import Revisionable
from runway.model_registry.values import ModelRegistryType
from runway.settings import (
    MLFlowModelRegistryData,
    RunwayLaunchParameters,
    RunwayModelRegistry,
    settings,
)


def log_runway_model_artifacts(
    model_info: ModelInfo,
    inputs_sample: ModelInputsSample = None,
    include_snapshot_image: bool = True,
    include_evaluate_model: bool = True,
) -> Revisionable:
    """runway model artifacts 을 생성한다."""
    # TODO 나중엔 optional 로 받을거라, keyword args 로 받지만 내부적으로는 positional args 로 예외처리
    if inputs_sample is None:
        raise ValueError("not allowed empty inputs_sample")
    if not mlflow.active_run():
        raise RuntimeError(f"not found active run: {mlflow.active_run()=}")

    if settings.launch_params is None:
        if settings.RUNWAY_LANUCH_PARAMETERS:
            settings.launch_params = RunwayLaunchParameters.parse_raw(
                settings.RUNWAY_LANUCH_PARAMETERS,
            )
            assert settings.launch_params
        else:
            # TODO: 적절한 exception으로 변경 필요
            raise ValueError("Launch params is not set")

    if settings.model_registry is None:
        if settings.RUNWAY_MODEL_REGISTRY:
            settings.model_registry = RunwayModelRegistry.parse_raw(
                settings.RUNWAY_MODEL_REGISTRY,
            )
            assert settings.model_registry
        else:
            # TODO: 적절한 exception으로 변경 필요
            raise ValueError("Model registry is not set")

    if not isinstance(settings.model_registry.data, MLFlowModelRegistryData):
        # TODO: 적절한 exception으로 변경 필요
        raise ValueError("Not enough model registry data to access mlflow")

    if not settings.RUNNING_IN_KUBERNETES:
        image_snapshot_info = ImageSnapshotInfo(image_url="", run_uuid="")
    elif isinstance(include_snapshot_image, bool) and include_snapshot_image:
        image_snapshot_info = snapshot_container_image(
            extract_essential_model_data(
                ModelRegistryType.mlflow,
                artifact_path=model_info.artifact_path,
                run_id=model_info.run_id,
            ),
            mlflow.active_run().info.run_name,  # type: ignore[union-attr]
        )
    elif include_snapshot_image == None:
        # NOTE debugging 용도로 image snapshot 을 force 수행한다.
        image_snapshot_info = snapshot_container_image(
            extract_essential_model_data(
                ModelRegistryType.mlflow,
                artifact_path=model_info.artifact_path,
                run_id=model_info.run_id,
            ),
            mlflow.active_run().info.run_name,  # type: ignore[union-attr]
            force=True,
        )

    # NOTE inputs_sample 가 method_name 이 없이 들어올 수 있다.
    framework = extract_framework_type_from(model_info)
    inputs_sample = fillout_inputs_sample(framework, inputs_sample)
    outputs_sample = None
    if include_evaluate_model:
        if inputs_sample is None:
            raise ValueError("not allowed empty inputs_sample to evaluate model")
        outputs_sample = evaluate_model(model_info, inputs_sample)

    # NOTE runway config 작성, 아래와 같이 값이 설정되어야 한다.
    model_artifacts = RunwayModelArtifacts.build(
        framework=framework,
        mlflow_model_info=model_info,
        inputs_sample=inputs_sample,
        outputs_sample=outputs_sample,
        image_snapshot_info=image_snapshot_info,
        artifact_size_bytes=get_artifact_size_bytes(mlflow.active_run(), model_info),
        launch_params=settings.launch_params,
    )

    # NOTE settings.model_registry.data token 정보가 login과 관련 및 mlflow 연결 시 필요할 수 있음
    model_artifacts.log(model_info)

    return model_artifacts


def log_model(
    model: Any,
    input_samples: ModelInputsSample,
    model_name: str = "model",
    include_snapshot_image: bool = True,
    image_url: Optional[str] = None,
    **kwargs: Unpack[Dict[str, Any]],
) -> ModelInfo:
    if not mlflow.active_run():
        raise RuntimeError(f"not found active run: {mlflow.active_run()=}")

    model_info = mlflow.pyfunc.log_model(model_name, python_model=model)
    include_evaluate_model = bool(kwargs.pop("include_evaluate_model", True))
    log_runway_model_artifacts(
        model_info,
        inputs_sample=input_samples,
        include_snapshot_image=include_snapshot_image,
        include_evaluate_model=include_evaluate_model,
    )

    return model_info
