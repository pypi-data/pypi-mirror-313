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
#
from typing import Any, Dict

from runway.common.api_client import api_client
from runway.settings import settings


def login_and_get_token(email: str, password: str) -> Dict[str, Any]:
    """Login and Get a SDK token."""
    api_client.base_url = (
        f"{settings.RUNWAY_API_PROTOCOL}://{settings.RUNWAY_API_SERVER_URL}"
    )
    response: Dict[str, Any] = api_client.post(
        endpoint="/v1/sdk/users/login",
        json_data={"email": email, "password": password},
    )
    return response


def logout_and_delete_token(token: str) -> None:
    """Logout and Delete a SDK token."""
    api_client.post(
        endpoint="/v1/sdk/users/logout",
        json_data={"token": token},
    )


def fetch_user_profile() -> Dict[str, Any]:
    """Get the profile of the user."""
    response: Dict[str, Any] = api_client.get(endpoint="/v1/sdk/users/user_profile")
    return response["user"]
