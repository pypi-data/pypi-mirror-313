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

from runway.common.enum_ import Enum, StrEnum, auto


class SchemaRevision(str, Enum):
    rev1 = "1"
    rev2 = "2"

    @classmethod
    def get_latest_revision(cls) -> "SchemaRevision":
        return max(SchemaRevision, key=lambda x: int(x.value))


class ModelRegistryType(StrEnum):
    """Supported Model Registry type."""

    mlflow = auto()
    wandb = auto()


class ModelFramework(StrEnum):
    """Supported Model Framework to log model."""

    onnx = auto()
    pytorch = auto()
    pyfunc = auto()
    sklearn = auto()
    tensorflow = auto()
    xgboost = auto()


# TODO 나중에는 kserve 의 "content_type" 처럼 "pd" 로 encoder 를 명시하는 방향으로 수정하자.
class DataSchemaType(str, Enum):
    column = "column"
    tensor = "tensor"

    # TODO: external or others
