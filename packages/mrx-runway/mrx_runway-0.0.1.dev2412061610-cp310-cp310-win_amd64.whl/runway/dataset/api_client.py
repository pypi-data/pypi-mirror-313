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
import base64
from typing import Any, BinaryIO, Dict, Final, Optional

from runway.common.api_client import api_client
from runway.common.utils import exception_handler, exclude_none
from runway.common.values import WorkloadType

# NOTE module-hierarchy 가 맞지 않기 때문에 rev2 보다 큰 revision 이 생성되면 수정되어야 한다.
from runway.settings import settings

REQUEST_TIMEOUT: Final[int] = 10


def sdk_upload_data_snapshot(
    name: str,
    filename: str,
    binary: BinaryIO,
    description: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Using SDK token, upload a new data snapshot in the current project
    """
    create_response = sdk_create_data_snapshot(name=name, description=description, exist_ok=True)
    data_snapshot_id: int = create_response["id"]

    # Upload metadata.
    api_path_format: str = "/v1/sdk/workspaces/{workspace_id}/projects/{project_id}/data-snapshots/{data_snapshot_id}/upload-metadata"
    api_path: str = api_path_format.format(
        workspace_id=settings.RUNWAY_WORKSPACE_ID,
        project_id=settings.RUNWAY_PROJECT_ID,
        data_snapshot_id=data_snapshot_id,
    )

    data: Dict[str, Any] = exclude_none({"description": description, "file_count": 1})

    response: Dict[str, Any] = api_client.post(endpoint=api_path, json_data=data)

    # Upload file.
    api_path_format = "/v1/sdk/workspaces/{workspace_id}/projects/{project_id}/data-snapshots/{data_snapshot_id}/upload"
    api_path = api_path_format.format(
        workspace_id=settings.RUNWAY_WORKSPACE_ID,
        project_id=settings.RUNWAY_PROJECT_ID,
        data_snapshot_id=data_snapshot_id,
    )

    response = api_client.post(
        endpoint=api_path,
        data=binary,
        headers={"Filename": base64.b64encode(filename.encode("utf-8")).decode("utf-8")},
    )

    return response


def internal_upload_data_snapshot(
    name: str,
    binary: BinaryIO,
    description: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Without any token, upload the new data snapshot in the current project.
    Intended to be used in the internal environment(pipeline).
    """
    api_path_format: str = "/v1/internal/workspaces/projects/{pid}/data-snapshots/sdk"
    api_path: str = api_path_format.format(pid=settings.RUNWAY_PROJECT_ID)

    data: Dict[str, Any] = exclude_none(
        {
            "user_id": settings.RUNWAY_USER_ID,
            "name": name,
            "description": description,
            "argo_workflow_run_id": settings.ARGO_WORKFLOW_RUN_ID,
        },
    )

    files: Dict[str, Any] = {"file": binary}

    response: Dict[str, Any] = api_client.post(endpoint=api_path, data=data, files=files)
    return response


def sdk_create_data_snapshot(
    name: str,
    description: Optional[str] = None,
    exist_ok: bool = False,
) -> dict:
    """
    Using SDK token, create a new data snapshot in the current project
    """

    api_path_format: str = "/v1/sdk/workspaces/{wid}/projects/{pid}/data-snapshots"
    api_path: str = api_path_format.format(
        wid=settings.RUNWAY_WORKSPACE_ID,
        pid=settings.RUNWAY_PROJECT_ID,
    )

    data = exclude_none(
        {
            "name": name,
            "description": description,
            "exist_ok": exist_ok,
        },
    )

    response: dict = api_client.post(api_path, json_data=data)

    return response


def internal_create_data_snapshot(
    name: str,
    description: Optional[str] = None,
    exist_ok: bool = False,
) -> dict:
    """
    Without any token, create the new data snapshot in the current project.
    Intended to be used in the internal environment(pipeline).
    """

    api_path_format: str = "/v1/internal/workspaces/projects/{pid}/data-snapshots"
    api_path: str = api_path_format.format(pid=settings.RUNWAY_PROJECT_ID)

    data = exclude_none(
        {
            "user_id": settings.RUNWAY_USER_ID,
            "name": name,
            "description": description,
            "exist_ok": exist_ok,
        },
    )

    response: dict = api_client.post(api_path, json_data=data)

    return response


def sdk_get_data_snapshot_by_name(name: str) -> dict:
    """
    Using SDK token, get a data snapshot by name.
    Name should be matched exactly
    """
    api_path_format: str = "/v1/sdk/workspaces/{wid}/projects/{pid}/data-snapshots/name"
    api_path: str = api_path_format.format(
        wid=settings.RUNWAY_WORKSPACE_ID,
        pid=settings.RUNWAY_PROJECT_ID,
    )

    params = {"name": name}

    response = api_client.get(api_path, params=params)

    return response


def internal_get_data_snapshot_by_name(name: str) -> dict:
    """
    Without any token, get the data snapshot in the current project.
    Intended to be used in the internal environment(pipeline).

    Name should be matched exactly
    """
    api_path_format: str = "/v1/internal/workspaces/projects/{pid}/data-snapshots/name"
    api_path: str = api_path_format.format(pid=settings.RUNWAY_PROJECT_ID)

    params = {"name": name, "user_id": settings.RUNWAY_USER_ID}

    response = api_client.get(api_path, params=params)

    return response


def sdk_create_data_snapshot_version(
    data_snapshot_id: int,
    description: Optional[str] = None,
) -> dict:
    """
    Using SDK token, create a new data snapshot version.
    """
    api_path_format: str = (
        "/v1/sdk/workspaces/{wid}/projects/{pid}/data-snapshots/{did}/versions"
    )
    api_path: str = api_path_format.format(
        wid=settings.RUNWAY_WORKSPACE_ID,
        pid=settings.RUNWAY_PROJECT_ID,
        did=data_snapshot_id,
    )

    data = exclude_none({"description": description})

    response: dict = api_client.post(api_path, json_data=data)

    return response


def sdk_get_data_snapshot_list() -> dict:
    api_path_format: str = "/v1/sdk/workspaces/{wid}/projects/{pid}/data-snapshots"
    api_path: str = api_path_format.format(
        wid=settings.RUNWAY_WORKSPACE_ID,
        pid=settings.RUNWAY_PROJECT_ID,
    )

    response: dict = api_client.get(api_path)

    return response


def sdk_get_data_snapshot_detail(data_snapshot_id: int) -> dict:
    api_path_format: str = (
        "/v1/sdk/workspaces/{wid}/projects/{pid}/data-snapshots/{did}"
    )
    api_path: str = api_path_format.format(
        wid=settings.RUNWAY_WORKSPACE_ID,
        pid=settings.RUNWAY_PROJECT_ID,
        did=data_snapshot_id,
    )

    response: dict = api_client.get(api_path)

    return response


def internal_create_data_snapshot_version(
    data_snapshot_id: int,
    description: Optional[str] = None,
) -> dict:
    """
    Without any token, create a new data snapshot version.
    Intended to be used in the internal environment(pipeline).
    """
    api_path_format: str = (
        "/v1/internal/workspaces/projects/{pid}/data-snapshots/{did}/versions"
    )
    api_path: str = api_path_format.format(
        pid=settings.RUNWAY_PROJECT_ID,
        did=data_snapshot_id,
    )

    data = exclude_none(
        {
            "user_id": settings.RUNWAY_USER_ID,
            "description": description,
            "argo_workflow_run_id": settings.ARGO_WORKFLOW,
        },
    )

    response: dict = api_client.post(api_path, json_data=data)

    return response


def sdk_get_code_snippet_to_upload_tabular_data_snapshot(
    name: str,
    data: str,
    file_type: str,
) -> dict:
    """
    Get code snippet to upload tabular data snapshot.
    """
    api_path_format: str = (
        "/v1/sdk/workspaces/{wid}/projects/{pid}/data-snapshots/tabular/code-snippet"
    )
    api_path: str = api_path_format.format(
        wid=settings.RUNWAY_WORKSPACE_ID,
        pid=settings.RUNWAY_PROJECT_ID,
    )

    params = {
        "name": name,
        "data": data,
        "file_type": file_type,
    }

    response: dict = api_client.get(api_path, params=params)

    return response


def sdk_get_code_snippet_to_import_data_snapshot(
    data_snapshot_id: int,
    data_snapshot_version_id: int,
) -> dict:
    """
    Get code snippet to import data snapshot.
    """

    api_path_format: str = "/v1/sdk/workspaces/{wid}/projects/{pid}/data-snapshots/{did}/versions/{vid}/code-snippet"
    api_path: str = api_path_format.format(
        wid=settings.RUNWAY_WORKSPACE_ID,
        pid=settings.RUNWAY_PROJECT_ID,
        did=data_snapshot_id,
        vid=data_snapshot_version_id,
    )

    response: dict = api_client.get(api_path)

    return response


def sdk_get_code_snippet_to_upload_tabular_data_snapshot(
    name: str,
    data: str,
    file_type: str,
) -> dict:
    """
    Get code snippet to upload tabular data snapshot.
    """
    api_path_format: str = (
        "/v1/sdk/workspaces/{wid}/projects/{pid}/data-snapshots/tabular/code-snippet"
    )
    api_path: str = api_path_format.format(
        wid=settings.RUNWAY_WORKSPACE_ID,
        pid=settings.RUNWAY_PROJECT_ID,
    )

    params = {
        "name": name,
        "data": data,
        "file_type": file_type,
    }

    response: dict = api_client.get(api_path, params=params)

    return response


def sdk_get_code_snippet_to_import_data_snapshot(
    data_snapshot_id: int,
    data_snapshot_version_id: int,
) -> dict:
    """
    Get code snippet to import data snapshot.
    """

    api_path_format: str = "/v1/sdk/workspaces/{wid}/projects/{pid}/data-snapshots/{did}/versions/{vid}/code-snippet"
    api_path: str = api_path_format.format(
        wid=settings.RUNWAY_WORKSPACE_ID,
        pid=settings.RUNWAY_PROJECT_ID,
        did=data_snapshot_id,
        vid=data_snapshot_version_id,
    )

    response: dict = api_client.get(api_path)

    return response
