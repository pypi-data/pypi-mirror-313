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
import logging
import os
import re
import site
from importlib import import_module
from pathlib import Path
from typing import Any, Dict, Final, Optional

import requests

from runway.common.values import WorkloadType
from runway.settings import settings

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT: Final[int] = 10


def is_http_url(value: str) -> bool:
    """return http url string."""
    pattern = re.compile(r"^https?://")
    return isinstance(value, str) and bool(pattern.match(value))


def import_module_from_path(file_path: Path) -> Any:
    """import module from path."""
    # import 하는 파일이 runway_taskflow 폴더 안에 있다면 ? 상대경로로 변환한다.
    for path in site.getsitepackages() + [site.getusersitepackages()]:
        try:
            file_path = file_path.relative_to(path)
        except ValueError:
            ...
    # unittest 와 같이 import 하는 파일이 현재 실행경로 안에 있다면 ? 상대경로로 변환한다.
    try:
        file_path = file_path.relative_to(os.getcwd())
    except ValueError:
        ...
    return import_module(".".join(file_path.parts[:]).rsplit(".", 1)[0])


def exception_handler(response: requests.Response) -> requests.Response:
    if not response.ok:
        code = response.json().get("code")
        raise requests.RequestException(
            f"response={response}, response.text={response.text}, response.code={code}",
        )
    return response


def exclude_none(d: Dict[str, Any]) -> Dict[str, Any]:
    """remove items that have none value."""
    return {k: v for k, v in d.items() if v is not None}


def get_runway_environment() -> str:
    """
    Get current execution environment has necessary Runway configurations.

    Returns:
        str: "dev-instance" if all required Runway settings are set, "runway-lite-client" otherwise
    """
    if all(
        getattr(settings, var, None) is not None
        for var in settings.Config.required_env_vars
    ):
        return "dev-instance"

    return "runway-lite-client"


def save_settings_to_dotenv() -> None:
    """Save settings to .mrx-runway.env file."""
    with open(
        settings.Config.env_file,
        mode="w",
        encoding=settings.Config.env_file_encoding,
    ) as writer:
        for key, value in settings.dict().items():
            if value in [None, "None"]:
                writer.write(f"{key}=''\n")
            else:
                writer.write(f"{key}={repr(value)}\n")


def inspect_workload_type() -> Optional[WorkloadType]:
    """
    Inspect workload type from settings.
    """

    if settings.launch_params is not None and settings.launch_params.source is not None:
        if settings.launch_params.source.entityname == WorkloadType.dev_instance:  # type: ignore[union-attr]
            return WorkloadType.dev_instance
        elif settings.launch_params.source.entityname == WorkloadType.pipeline:  # type: ignore[union-attr]
            return WorkloadType.pipeline

    return None
