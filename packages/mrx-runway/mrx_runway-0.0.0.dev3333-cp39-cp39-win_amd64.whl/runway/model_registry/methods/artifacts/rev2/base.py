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
import tempfile
from pathlib import Path
from typing import Any, Optional, Union, get_args, get_origin

import mlflow
from mlflow.models.model import ModelInfo

from ....schemas import (
    IOSample,
    ModelConfig,
    Revision,
    Revisionable,
    RevisionableSchema,
)


class ModelArtifacts(RevisionableSchema):
    # NOTE revision field 는 non-inherited 이고 재정의 변수이기에, ClassVar 를 쓰지 않는다.
    revision: Revision  # type: ignore
    # NOTE pydantic v2 부터는 model_config 를 field name 으로 지정할 수 없다.
    model_config: ModelConfig  # type: ignore
    io_sample: Optional[IOSample] = None

    def log(self, model_info: ModelInfo) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            for key in self.__fields__:
                obj = getattr(self, key)
                if not isinstance(obj, RevisionableSchema):
                    continue
                if not (hasattr(obj, "schema_name") and hasattr(obj, "revision")):
                    # RevisionableSchema를 상속한 중간 parent class가 정의될 수 있으므로
                    # 이를 구분하기 위하여 최종적으로 schema_name과 revision 모두 존재하는 경우를 구분
                    # ex) ModelConfig parent class는 schema_name은 정의하나 revision attr을 정의하지 않음
                    continue
                filename = Path(tmp_dir) / obj.get_filename()
                with open(filename, "w") as file:
                    obj.dump(file)
                mlflow.log_artifact(str(filename), artifact_path=str(model_info.artifact_path))

    @classmethod
    def parse(cls, path: Union[str, Path]) -> Revisionable:
        if isinstance(path, str):
            path = Path(path)

        fields = {}
        for key, obj in cls.__fields__.items():
            c = (
                get_args(obj.annotation)[0]
                if cls.is_optional_type(obj.annotation)
                else obj.annotation
            )
            if not issubclass(c, RevisionableSchema):
                continue

            filename = path / c.get_filename()
            if not filename.exists():
                continue
            with open(filename, "r") as file:
                fields[key] = c.load(file)

        return ModelArtifacts(**fields)

    @classmethod
    def build(cls, context: Revisionable.BuilderContext) -> "Revisionable":
        return ModelArtifacts(
            revision=Revision.build(context),
            model_config=ModelConfig.build(context),
            io_sample=IOSample.build(context),
        )

    @staticmethod
    def is_optional_type(tp: Any) -> bool:
        if get_origin(tp) is Union:
            args = get_args(tp)
            return len(args) == 2 and type(None) in args
        return False
