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
import inspect
import logging
from typing import Any, List

logger = logging.getLogger(__name__)


def inspect_method_list(obj: Any) -> List[str]:
    """return the list of method_name of all methods of the object."""
    method_list: List[Any] = []
    try:
        method_list: List[Any] = list(zip(*inspect.getmembers(obj, inspect.ismethod)))
        if method_list:
            return list(method_list[0])
    except Exception as e:
        logger.warning(e)

    """
        Cpython 을 이용한 class 인 경우 아래와 같이 TypeError 가 난다.
        TypeError: The classmethod `LitModel.load_from_checkpoint` cannot be called on an instance.
        Please call it on the class type and make sure the return value is used.
    """
    method_names: List[str] = []
    for name in dir(obj):
        try:
            if inspect.ismethod(getattr(obj, name)):
                method_names.append(name)
        except Exception as e:
            """
            pytorch-lightning 의 경우, 아래 classmethod 관련 error 발생.
            - The classmethod `LitModel.load_from_checkpoint` cannot be called on an instance. Please call it on the class type and make sure the return value is used.
            """
            logger.warning(e)

    return method_names


def has_method_names(obj: Any, method_names: List[str]) -> None:
    """check that the object has method names."""
    inspected_methods = inspect_method_list(obj)
    for method in method_names:
        if method not in inspected_methods:
            raise AttributeError(f"method ({method}) is not defined in the model")
