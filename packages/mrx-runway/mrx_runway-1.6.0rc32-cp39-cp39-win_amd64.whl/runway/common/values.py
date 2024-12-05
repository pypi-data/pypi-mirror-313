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

class WorkloadType(str, Enum):
    """
    links, training_runs are from table name
    - runway_core.links.models.Link
    - runway_core.training_pipelines.models.TrainingRun
    """

    dev_instance = "dev_instance"
    pipeline = "pipeline"
    # TODO: external or others


class DatabaseType(StrEnum):
    """backend supported database types"""

    postgresql = auto()
    mysql = auto()
    oracle = auto()
    mssql = auto()
    tibero = auto()

class StorageType(StrEnum):
    """
    backend supported storage types
    """

    aws = auto()
    minio = auto()
    nfs = auto()
    azure = auto()
    gcp = auto()
