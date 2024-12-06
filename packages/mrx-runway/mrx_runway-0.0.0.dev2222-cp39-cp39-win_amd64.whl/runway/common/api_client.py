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

import urllib.parse
from typing import Any, Dict, Optional

import requests

from runway.common.utils import REQUEST_TIMEOUT, exception_handler
from runway.settings import settings


class APIClient:
    def __init__(self) -> None:
        self.base_url = (
            f"{settings.RUNWAY_API_PROTOCOL}://{settings.RUNWAY_API_SERVER_URL}"
        )
        self.timeout = REQUEST_TIMEOUT
        self.exception_handler = exception_handler

    @property
    def headers(self) -> Dict[str, str]:
        if settings.TOKEN:
            return {"Authorization": f"Bearer {settings.TOKEN}"}

        return {"Authorization": f"Bearer {settings.RUNWAY_SDK_TOKEN}"}

    def _build_url(self, endpoint: str) -> str:
        return urllib.parse.urljoin(self.base_url, endpoint)

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = self._build_url(endpoint)
        response = self.exception_handler(
            requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=self.timeout,
            ),
        )
        return response.json()

    def post(
        self,
        endpoint: str,
        data: Optional[Any] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = self._build_url(endpoint)
        request_headers: Dict[str, Any] = {**self.headers, **headers} if headers else self.headers

        response = self.exception_handler(
            requests.post(
                url=url,
                data=data,
                json=json_data,
                headers=request_headers,
                files=files,
                timeout=self.timeout,
            ),
        )

        return response.json()


api_client = APIClient()
