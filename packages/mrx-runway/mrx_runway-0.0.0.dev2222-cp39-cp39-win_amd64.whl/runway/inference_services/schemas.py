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

from runway.common.schemas import BasePydanticInfo
from typing import Union
from runway.inference_services.values import (
    InferenceDatabaseRecordsMatchType,
    InferenceDatabaseRecordsSortOrderType,
    InferenceServiceLoggerType,
)
from typing import List, Optional

class OwnerData(BasePydanticInfo):
    """Owner data"""
    id: int
    first_name: str
    last_name: str
    email: str

class TagData(BasePydanticInfo):
    """Tag data"""
    id: int
    name: str

class LoggerConnectionDatabaseConfig(BasePydanticInfo):
    """Database storage configuration"""
    type: str
    host: str
    port: str
    user: str
    password: str
    database: str
    table: str

class Logger(BasePydanticInfo):
    """Logger configuration"""
    id: int
    type: InferenceServiceLoggerType
    connection_config: Union[LoggerConnectionDatabaseConfig]
    # TODO: add other ConnectionConfgClasses in Union when implementing other type of loggers

class Serving(BasePydanticInfo):
    """Serving configuration"""
    id: int
    enable_logger: bool
    loggers: List[Logger]

class InferenceRecordsSorting(BasePydanticInfo):
    """Inference logging sorting"""
    order_type: InferenceDatabaseRecordsSortOrderType

class InferenceDatabaseRecordsSorting(InferenceRecordsSorting):
    """DB inference logging sorting"""
    column_name: str

class InferenceDatabaseRecordsFilter(BasePydanticInfo):
    """DB inference logging filter"""
    column_name: str
    match_type: InferenceDatabaseRecordsMatchType
    match_value: Union[str, int, bool]

class InferenceDatabaseRecordsQuery(BasePydanticInfo):
    """Basic DB query options with sorting, filtering, and pagination"""
    sorting: List[InferenceDatabaseRecordsSorting]
    filters: Optional[List[InferenceDatabaseRecordsFilter]] = None
    offset: int = 0
    limit: int = 100
