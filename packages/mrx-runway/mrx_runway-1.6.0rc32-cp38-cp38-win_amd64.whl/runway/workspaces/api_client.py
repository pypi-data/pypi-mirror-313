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


def fetch_joined_workspaces() -> List[Dict[str, Any]]:
    response = api_client.get("/v1/sdk/users/workspaces")
    return response["workspaces"]


def fetch_user_role_in_workspace(workspace_id: int) -> Dict[str, Any]:
    """Get the role of the workspace user."""
    response: Dict[str, Any] = api_client.get(
        endpoint=f"/v1/sdk/workspaces/{workspace_id}/users/user_role",
    )
    return response
