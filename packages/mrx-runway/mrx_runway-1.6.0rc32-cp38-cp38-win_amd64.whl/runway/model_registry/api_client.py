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

from typing import Any, Dict, List, Optional

from runway.common.api_client import api_client
from runway.settings import settings


def fetch_model_registry_list(
    params: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    response = api_client.get(
        f"/v1/sdk/workspaces/{settings.RUNWAY_WORKSPACE_ID}/projects/{settings.RUNWAY_PROJECT_ID}/model-registries",
        params=params,
    )
    return response["model_registries"]


def fetch_model_registry(model_registry_id: int) -> Dict[str, Any]:
    response = api_client.get(
        f"/v1/sdk/workspaces/{settings.RUNWAY_WORKSPACE_ID}/projects/{settings.RUNWAY_PROJECT_ID}/model-registries/{model_registry_id}",
    )
    return response
