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
from typing import Any, BinaryIO, Dict, Final, Optional

import requests
from pydantic import BaseModel, Field

from runway.common.utils import exception_handler

# NOTE module-hierarchy 가 맞지 않기 때문에 rev2 보다 큰 revision 이 생성되면 수정되어야 한다.
from runway.settings import settings

REQUEST_TIMEOUT: Final[int] = 10


class ImageSnapshotInfo(BaseModel):
    image_url: str
    run_uuid: str = Field(..., description="image snapshot uuid created by runway")


def create_image_snapshot(
    repository_name: str,
    extra: Optional[Dict[Any, Any]] = None,
    force: Optional[bool] = None,
) -> ImageSnapshotInfo:
    """image snapshot 을 만든다."""
    if settings.launch_params is None:
        raise ValueError("There are no launch parameters")

    data: Dict[str, Any] = {"repository_name": repository_name}
    if settings.RUNWAY_PROJECT_ID:
        data["project_id"] = int(settings.RUNWAY_PROJECT_ID)
    if settings.container_registry:
        data["container_registry_id"] = settings.container_registry.id
    if settings.launch_params.notebook_name:
        data["notebook_name"] = settings.launch_params.notebook_name
    if settings.launch_params.container_image_name:
        data["pipeline_image_name"] = settings.launch_params.container_image_name
    if settings.launch_params.source:
        data["source_name"] = settings.launch_params.source.entityname
    if extra:
        data["extra"] = extra
    if force:
        data["force"] = force

    response = exception_handler(
        requests.post(
            f"http://{settings.RUNWAY_API_SERVER_URL}/v1/image-snapshots/image-registry",
            headers={"Authorization": f"Bearer {settings.RUNWAY_AUTH_BEARER_TOKEN}"},
            json=data,
        ),
    )

    return ImageSnapshotInfo(**response.json())
