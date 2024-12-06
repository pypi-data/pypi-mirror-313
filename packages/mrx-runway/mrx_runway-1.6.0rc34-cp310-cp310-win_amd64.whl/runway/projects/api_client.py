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

from typing import Any, Dict, List

from runway.common.api_client import api_client
from runway.settings import settings


def fetch_joined_projects() -> List[Dict[str, Any]]:
    response = api_client.get(
        f"/v1/sdk/workspaces/{settings.RUNWAY_WORKSPACE_ID}/projects",
    )
    return response["projects"]


def fetch_user_project_role(project_id: int) -> Dict[str, Any]:
    response = api_client.get(
        f"/v1/sdk/workspaces/{settings.RUNWAY_WORKSPACE_ID}/projects/{project_id}/users/user_role",
    )
    return response["user"]
