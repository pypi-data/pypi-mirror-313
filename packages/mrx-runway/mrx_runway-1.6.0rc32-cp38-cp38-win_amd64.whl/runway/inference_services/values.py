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

from runway.common.enum_ import StrEnum, auto

class InferenceServiceLoggerType(StrEnum):
    """Enum class for inference service logger types

    Attributes
    ----------
    external : str
        External logger type
    internal : str
        Internal logger type
    """
    external = auto()
    internal = auto()

class InferenceDatabaseRecordsMatchType(StrEnum):
    """Enum class for database query match types

    Attributes
    ----------
    eq : str
        Equal to
    like : str
        Pattern matching using LIKE operator
    gt : str
        Greater than
    lt : str
        Less than
    gte : str
        Greater than or equal to
    lte : str
        Less than or equal to
    ne : str
        Not equal to
    """
    eq = auto()
    like = auto()
    gt = auto()
    lt = auto()
    gte = auto()
    lte = auto()
    ne = auto()

class InferenceDatabaseRecordsSortOrderType(StrEnum):
    """Enum class for sort order types

    Attributes
    ----------
    asc : str
        Ascending order
    desc : str
        Descending order
    """
    asc = auto()
    desc = auto()
