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

def fetch_inference_services(name: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
    """Fetch inference services from the API.

    Parameters
    ----------
    name : Optional[str]
        Filter services by name

    Returns
    -------
    Optional[List[Dict[str, Any]]]
        List of inference services or None if no services are found
    """
    endpoint = (
        f"/v1/sdk/workspaces/{settings.RUNWAY_WORKSPACE_ID}/projects/"
        f"{settings.RUNWAY_PROJECT_ID}/inference-services"
    )

    params = {"name": name} if name else None

    response = api_client.get(endpoint=endpoint, params=params)
    return response["inference_services"]
