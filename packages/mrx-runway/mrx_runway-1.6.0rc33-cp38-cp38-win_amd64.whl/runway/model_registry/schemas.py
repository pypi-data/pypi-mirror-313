# MAKINAROCKS CONFIDENTIAL
# ________________________
#
# [2017] - [2024] MakinaRocks Co., Ltd.
# All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of MakinaRocks Co., Ltd. and its suppliers, if any.
# The intellectual and technical concepts contained herein are
# proprietary to MakinaRocks Co., Ltd. and its suppliers and may be
# covered by U.S. and Foreign Patents, patents in process, and
# are protected by trade secret or copyright law. Dissemination
# of this information or reproduction of this material is
# strictly forbidden unless prior written permission is obtained
# from MakinaRocks Co., Ltd.

import abc
import io
import json
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Union,
)

import numpy as np
import pandas as pd
from mlflow.types.schema import DataType
from mlflow.types.utils import (
    _get_tensor_shape,
    _infer_pandas_column,
    clean_tensor_type,
)
from pydantic import BaseModel, Field, validator

from runway.common.schemas import BaseInfo
from runway.common.values import WorkloadType
from runway.model_registry.methods.artifacts.common import (
    CustomEncoder,
    extract_model_path_from_mlflow,
    stringify_io_name_by_module,
)
from runway.model_registry.values import DataSchemaType, ModelFramework, SchemaRevision

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class MLFlowEssentialData(BaseModel):
    type: Literal["mlflow"]
    artifact_path: str
    run_id: str


class WandbEssentialData(BaseModel):
    type: Literal["wandb"]


class ColumnSpecModel(BaseModel):
    """Column spec model."""

    name: Optional[str]
    dtype: str
    shape: Optional[List[int]] = [1]


class TensorSpecModel(BaseModel):
    """Tensor spec model."""

    name: Optional[str]
    dtype: str
    shape: List[int]


class RunwayParamModel(BaseModel):
    """Runway input model."""

    type: str
    # Field name `schema` shadows the field name in BaseModel
    schema_: List[Union[ColumnSpecModel, TensorSpecModel]] = Field(..., alias="schema")


class RunwaySignatureModel(BaseModel):
    """Runway signature model."""

    inputs: List[RunwayParamModel]
    outputs: List[RunwayParamModel]


RunwaySignatures = Dict[str, RunwaySignatureModel]


class ModelFlavorsModel(BaseModel):
    model_path: str
    framework: Union[str, ModelFramework]


class RunwayConfigModel(BaseModel):
    flavors: ModelFlavorsModel
    signatures: RunwaySignatures


class Revisionable(abc.ABC):
    class BuilderContext(SimpleNamespace):
        ...

    def dump(self, fp: io.TextIOWrapper) -> None:
        json.dump(self.to_dict(), fp, cls=CustomEncoder)

    @classmethod
    @abc.abstractmethod
    def load(self, fp: io.TextIOWrapper) -> "Revisionable":
        ...

    @abc.abstractmethod
    def to_dict(self) -> Dict:
        ...

    @abc.abstractmethod
    def from_dict(self, item: Dict) -> "Revisionable":
        ...

    @classmethod
    @abc.abstractmethod
    def build(cls, context: BuilderContext) -> "Revisionable":
        ...

    @classmethod
    def get_filename(cls) -> str:
        schema_name = cls.get_schema_name()
        if not schema_name:
            raise ValueError(f"not allowed empty schema_name")
        return schema_name + ".json"

    @classmethod
    def extract_schema_name_from_filename(cls, filename: str) -> Optional[str]:
        """
        저장된 Artifact에서 python 객체를 복구할 때 필요합니다
        schema_name이 올바르지 않은 경우 None을 반환합니다
        """
        return filename.rstrip(".json") if filename.endswith(".json") else None

    @classmethod
    @abc.abstractmethod
    def get_schema_name(cls) -> str:
        ...


class RevisionableSchema(Revisionable, BaseModel):
    schema_name: ClassVar[str]
    revision: ClassVar[SchemaRevision]  # type: ignore

    class Config:
        use_enum_values = True

    def to_dict(self) -> Dict[str, Any]:
        return self.dict(by_alias=True)

    @classmethod
    def load(cls, fp: io.TextIOWrapper) -> "Revisionable":
        return cls.parse_obj(json.load(fp))

    def from_dict(self, item: Dict[str, Any]) -> "Revisionable":
        return self.parse_obj(item)

    @classmethod
    def build(cls, context: Revisionable.BuilderContext) -> "Revisionable":
        raise NotImplementedError

    @classmethod
    def get_schema_name(cls) -> str:
        return cls.schema_name


class Revision(RevisionableSchema):
    schema_name: ClassVar[str] = "runway_revision"
    # NOTE revision field 는 non-inherited 이고 재정의 변수이기에, ClassVar 를 쓰지 않는다.
    revision: SchemaRevision  # type: ignore[misc]

    @classmethod
    def parse(cls, path: Union[str, Path]) -> Revisionable:
        if isinstance(path, str):
            path = Path(path)

        with open(path / cls.get_filename(), "r") as file:
            return Revision.load(file)

    @classmethod
    def build(cls, context: Revisionable.BuilderContext) -> "Revision":
        return Revision(revision=getattr(context, "revision"))


class ModelInfo(BaseModel):
    created_at: int  # unixtimestamp
    artifact_size: Optional[int]  # bytes


class RunwayImageSnapshotService(BaseModel):
    """
    'image_snapshots' is from runway_app.image_snapshots.ImageSnapshot's table name
    """

    name: Literal["image_snapshots"]
    resource_uuid: str


class RuntimeContainer(BaseModel):
    """
    Specify a runtime container spec for serving env construction

    image_url: str
        docker image
    service: RunwayImageSnapshotService
        - indicates corresponding managed entity in runway for image_url
        - to trace info about image such as build status, etc.
    """

    image_url: str
    service: RunwayImageSnapshotService


class SourceWorkload(BaseModel):
    """
    Specify on which workload the target model was trained for traceability
    - SourceWorkload's child classes should contains enough information
        to reproduce training env as much as possible
    """


class LinkWorkload(SourceWorkload):
    entityname: Literal[WorkloadType.dev_instance]
    resource_id: int
    dev_instance_type: Optional[str]


class TrainingRunWorkload(SourceWorkload):
    entityname: Literal[WorkloadType.pipeline]
    resource_id: int
    run_uuid: Optional[str]
    pipeline_id: Optional[int]
    pipeline_version_id: Optional[int]


class ModelExtensions(BaseModel):
    model_info: ModelInfo
    container: RuntimeContainer
    source: Optional[Union[LinkWorkload, TrainingRunWorkload]] = Field(
        ...,
        discriminator="entityname",
    )
    runway_sdk_version: Optional[str] = None  # TODO: need format checking?

    @classmethod
    def build(cls, context: Revisionable.BuilderContext) -> "ModelExtensions":
        if not hasattr(context, "mlflow_model_info"):
            raise ValueError(
                f"not found mlflow_model_info in builder context: {context=}",
            )
        if not hasattr(context, "image_snapshot_info"):
            raise ValueError(
                f"not found image_snapshot_info in builder context: {context=}",
            )
        if not hasattr(context, "artifact_size_bytes"):
            raise ValueError(
                f"not found artifact_size_bytes in builder context: {context=}",
            )
        if not hasattr(context, "launch_params"):
            raise ValueError(f"not found launch_params in builder context: {context=}")

        source: Optional[Union[LinkWorkload, TrainingRunWorkload]] = None
        if context.launch_params.source is not None:
            if context.launch_params.source.entityname == WorkloadType.dev_instance:
                source = LinkWorkload(**context.launch_params.source.dict())
            elif context.launch_params.source.entityname == WorkloadType.pipeline:
                source = TrainingRunWorkload(**context.launch_params.source.dict())
            else:
                raise ValueError(
                    "entity name of launch parameters should be in [dev_instance, pipeline]",
                )

        return ModelExtensions(
            model_info=ModelInfo(
                created_at=int(datetime.now().timestamp()),
                artifact_size=context.artifact_size_bytes,
            ),
            container=RuntimeContainer(
                image_url=context.image_snapshot_info.image_url,
                service=RunwayImageSnapshotService(
                    name="image_snapshots",
                    resource_uuid=context.image_snapshot_info.run_uuid,
                ),
            ),
            source=source,
        )


class ModelFlavors(BaseModel):
    model_path: str
    framework: Union[str, ModelFramework]

    @classmethod
    def build(cls, context: Revisionable.BuilderContext) -> "ModelFlavors":
        # TODO 나중에 wandb 가 들어온다면 abstraction 된 variable 로 받는게 좋다.
        if not hasattr(context, "mlflow_model_info"):
            raise ValueError(
                f"not found mlflow_model_info in builder context: {context=}",
            )
        if not hasattr(context, "framework"):
            raise ValueError(f"not found framework in builder context: {context=}")

        return ModelFlavors(
            model_path=extract_model_path_from_mlflow(
                context.mlflow_model_info,
                context.framework,
            ),
            framework=context.framework,
        )


class SchemaSpec(BaseModel):
    name: Optional[str]
    dtype: Union[str, DataType]
    shape: Optional[List[int]]  # TODO: validation?

    @validator("name")
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v == "":
            raise ValueError("Name is empty string")
        return v if v is not None else v


class ColumnSpec(SchemaSpec):
    shape: Optional[List[int]] = [1]

    @validator("shape")
    def validate_shape(cls, v: Optional[List[int]]) -> Optional[List[int]]:
        if v is not None and v != [1]:
            raise ValueError(
                "Shape of '%s' type schema should be [1]" % DataSchemaType.column,
            )
        return v


class TensorSpec(SchemaSpec):
    shape: List[int]


class DataSchema(BaseModel, abc.ABC):
    """
    24.04.23)
    * mlflow signature: https://mlflow.org/docs/latest/model/signatures.html#id1
    * runway에서는 단순한 List[SchemaSpec]인 mlflow와 달리 DataSchema에도 name을 부여됩니다
    * 이것은 여러 개의 input을 허용하는 v2 inference protocol에 기반한 추론 서비스를 생성하여 사용하기 때문입니다
        - https://kserve.github.io/website/0.8/modelserving/inference_api/#inference-request-json-object
    """

    name: str
    type: Literal[DataSchemaType.column, DataSchemaType.tensor]
    # Field name `schema` shadows the field name in BaseModel
    schema_: Sequence[SchemaSpec] = Field(..., alias="schema")

    class Config:
        # to allow {'schema_': [...], ...} (required for save/restore scenario)
        allow_population_by_field_name = True


class ColumnDataSchema(DataSchema):
    type: Literal[DataSchemaType.column]
    schema_: Sequence[ColumnSpec] = Field(..., alias="schema")

    @validator("schema_")
    def validate_schema(cls, v: Sequence[ColumnSpec]) -> Sequence[ColumnSpec]:
        schema_names = list(map(lambda x: getattr(x, "name", None), v))
        if len(set(map(lambda x: x is None, schema_names))) == 2:
            raise ValueError(
                "Either all or none of the schema should have names: %s" % v,
            )

        is_named_schema = schema_names[0] is not None
        if is_named_schema and (len(set(schema_names)) != len(schema_names)):
            raise ValueError("Duplicated names in the schema: %s" % v)

        return v


class TensorDataSchema(DataSchema):
    type: Literal[DataSchemaType.tensor]
    schema_: Sequence[TensorSpec] = Field(..., alias="schema")

    @validator("schema_")
    def validate_schema(cls, v: Sequence[ColumnSpec]) -> Sequence[ColumnSpec]:
        schema_names = list(map(lambda x: getattr(x, "name", None), v))
        if len(set(map(lambda x: x is None, schema_names))) == 2:
            raise ValueError(
                "Either all or none of the schema should have names: %s" % v,
            )

        is_named_schema = schema_names[0] is not None
        if is_named_schema and (len(set(schema_names)) != len(schema_names)):
            raise ValueError("Duplicated names in the schema: %s" % v)

        if not is_named_schema and len(v) > 1:
            raise ValueError(
                "Tensor name is needed when there are more than one tensors: %s" % v,
            )

        return v


class ModelSignature(BaseModel):
    """
    24.04.22)
    * type annotation의 경우는 mlflow==2.12.1 버전 기준,
        mlflow.types.schema.Schema, mlflow.models.signature.ModelSignature를 참고하였습니다
        - inputs의 schema는 모두 Column 형식이거나 Tensor 형식이어야 한다
        - inputs, outputs schema의 형식이 같은지는 확인하지 않는다
    * 기존 runway_app.common.runway_signature에서 관련 로직은 찾지 못하였습니다
    * 다만 모두 Column이거나 Tensor라는 조건이 이상적인가는 얘기해볼 여지가 있을 것 같습니다
        - tabular 데이터는 보통 Column, image 데이터는 Tensor를 활용하는 것이 일반적
            - 두 가지 모두 활용하는 경우라면?
    """

    inputs: Union[List[ColumnDataSchema], List[TensorDataSchema]]
    outputs: Union[List[ColumnDataSchema], List[TensorDataSchema]]

    @validator("inputs", "outputs")
    def validate_unique_name(
        cls,
        v: Union[List[ColumnDataSchema], List[TensorDataSchema]],
    ) -> Union[List[ColumnDataSchema], List[TensorDataSchema]]:
        schema_names = list(map(lambda x: x.name, v))
        if len(set(schema_names)) != len(schema_names):
            raise ValueError("Duplicated names in the schema list: %s" % v)

        return v

    @classmethod
    def build(cls, context: Revisionable.BuilderContext) -> Dict[str, "ModelSignature"]:
        if not hasattr(context, "mlflow_model_info"):
            raise ValueError(
                f"not found mlflow_model_info in builder context: {context=}",
            )
        if not hasattr(context, "inputs_sample"):
            raise ValueError(f"not found inputs_sample in builder context: {context=}")
        if not hasattr(context, "framework"):
            raise ValueError(f"not found framework in builder context: {context=}")

        signatures = {}
        for method_name, input_sample in context.inputs_sample.items():
            inputs = [
                cls.generate_io_field(
                    stringify_io_name_by_module(
                        "input",
                        idx,
                        context.framework,
                        context.mlflow_model_info,
                    ),
                    sample,
                )
                for idx, sample in enumerate(input_sample)
            ]

            outputs = None
            output_sample = getattr(context, "outputs_sample", {}).get(method_name)
            if output_sample:
                outputs = [
                    cls.generate_io_field(
                        stringify_io_name_by_module(
                            "output",
                            idx,
                            context.framework,
                            context.mlflow_model_info,
                        ),
                        sample,
                    )
                    for idx, sample in enumerate(output_sample)
                ]

            signatures[method_name] = ModelSignature(inputs=inputs, outputs=outputs)

        return signatures

    # TODO 나중에 관련 BaseModel 쪽으로 옮겨야 한다.
    @staticmethod
    def generate_io_field(
        name: str,
        sample: Union[pd.DataFrame, pd.Series, np.ndarray],
    ) -> Union[ColumnDataSchema, TensorDataSchema]:
        if isinstance(sample, pd.DataFrame):
            return ColumnDataSchema(
                type=DataSchemaType.column,
                name=name,
                schema_=[
                    ColumnSpec(
                        name=column,
                        dtype=_infer_pandas_column(sample[column]),
                    )
                    for column in sample
                ],
            )
        elif isinstance(sample, pd.Series):
            return ColumnDataSchema(
                type=DataSchemaType.column,
                name=name,
                schema_=[ColumnSpec(name=name, dtype=_infer_pandas_column(sample))],
            )
        elif isinstance(sample, np.ndarray):
            return TensorDataSchema(
                type=DataSchemaType.tensor,
                name=name,
                schema_=[
                    TensorSpec(
                        name=name,
                        dtype=str(clean_tensor_type(sample.dtype)),
                        shape=_get_tensor_shape(sample),
                    ),
                ],
            )

        raise ValueError(f"unknown sample type: type={type(sample)}")


class ModelConfig(RevisionableSchema):
    schema_name: ClassVar[str] = "runway_model_config"
    revision: ClassVar[SchemaRevision] = SchemaRevision.rev2
    flavors: ModelFlavors
    signatures: Mapping[str, ModelSignature]
    extensions: Optional[ModelExtensions] = None

    @validator("signatures")
    def validate_method_name(
        cls,
        v: Mapping[str, ModelSignature],
    ) -> Mapping[str, ModelSignature]:
        if not all(method_name.isidentifier() for method_name in v.keys()):
            raise ValueError(
                "Key names in signatures should take a form of python method name",
            )
        return v

    @classmethod
    def build(cls, context: Revisionable.BuilderContext) -> "ModelConfig":
        return ModelConfig(
            flavors=ModelFlavors.build(context),
            signatures=ModelSignature.build(context),
            extensions=ModelExtensions.build(context),
        )


class IOField(BaseModel):
    name: str
    data: Union[List, Union[Dict, Any]]


class IOSignature(BaseModel):
    inputs: Sequence[Any]
    outputs: Optional[Sequence[Any]]


class IOSample(RevisionableSchema):
    revision: ClassVar[SchemaRevision] = SchemaRevision.rev2
    schema_name: ClassVar[str] = "runway_io_sample"
    signatures: Mapping[str, IOSignature]

    @classmethod
    def build(cls, context: Revisionable.BuilderContext) -> "IOSample":
        if not hasattr(context, "mlflow_model_info"):
            raise ValueError(
                f"not found mlflow_model_info in builder context: {context=}",
            )
        if not hasattr(context, "inputs_sample"):
            raise ValueError(f"not found inputs_sample in builder context: {context=}")
        if not hasattr(context, "framework"):
            raise ValueError(f"not found framework in builder context: {context=}")

        signatures = {}
        for method_name, input_sample in context.inputs_sample.items():
            inputs = [
                cls.generate_io_field(
                    sample,
                    stringify_io_name_by_module(
                        "input",
                        idx,
                        context.framework,
                        context.mlflow_model_info,
                    ),
                )
                for idx, sample in enumerate(input_sample)
            ]

            outputs = None
            output_sample = getattr(context, "outputs_sample", {}).get(method_name)
            if output_sample:
                outputs = [
                    cls.generate_io_field(
                        sample,
                        stringify_io_name_by_module(
                            "input",
                            idx,
                            context.framework,
                            context.mlflow_model_info,
                        ),
                    )
                    for idx, sample in enumerate(output_sample)
                ]

            signatures[method_name] = IOSignature(inputs=inputs, outputs=outputs)

        return IOSample(signatures=signatures)

    # TODO 나중에 관련 BaseModel 쪽으로 옮겨야 한다.
    @staticmethod
    def generate_io_field(
        sample: Union[pd.DataFrame, np.ndarray, pd.Series, str, bytes],
        name: str,
    ) -> IOField:
        if isinstance(sample, pd.DataFrame):
            return IOField(
                name=name,
                data=[
                    {
                        "name": column,
                        "data": [sample[column].to_list()[0]],
                    }
                    for column in sample
                ],
            )
        if isinstance(sample, pd.Series):
            return IOField(
                name=name,
                data=[sample.to_list()[0]],
            )
        if isinstance(sample, np.ndarray):
            return IOField(
                name=name,
                # NOTE 애매하다. column type 일 경우 name - value 가 pair 이기에
                # data 아래 array 가 들어가야 하지만, tensor type 일 경우
                # value only 이기에 name 을 임의로 만들어야 한다.
                # signatures.json schema 가 내부 속성에 따라 변경되는 건 혼란스럽기에
                # 현행 유지한다.
                data=[dict(name=name, data=sample.tolist())],
            )

        raise ValueError(f"unknown sample type: type={type(sample)}")


class ModelRegistryInfo(BaseInfo):
    """ModelRegistry information."""

    pass
