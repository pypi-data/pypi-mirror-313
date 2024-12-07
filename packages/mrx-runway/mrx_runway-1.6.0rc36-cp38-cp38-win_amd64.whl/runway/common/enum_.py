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

from enum import Enum, auto
from typing import Any, List

_ = auto


class StrEnum(str, Enum):
    """
    Mixin class for using auto()
    """

    @staticmethod
    def _generate_next_value_(
        name: str,
        start: int,
        count: int,
        last_values: List[Any],
    ) -> str:
        """
        Ref: https://docs.python.org/3/library/enum.html#supported-sunder-names
        Used by auto to get an appropriate value for an enum member
        """
        _ = start, count, last_values

        return name

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

    @classmethod
    def has_value(cls, value: str) -> bool:
        """Check if the value is in the enum

        Parameters
        ----------
        value : str
            The value to check

        Returns
        -------
        bool
            True if the value is in the enum, False otherwise

        Examples
        --------
        >>> from runway.common.enum import StrEnum
        >>> class MyEnum(StrEnum):
        ...     A = auto()
        ...     B = auto()
        ...     C = auto()
        ...
        >>> MyEnum.has_value('A')
        True
        """
        return value in cls._value2member_map_  # pylint: disable=maybe-no-member
