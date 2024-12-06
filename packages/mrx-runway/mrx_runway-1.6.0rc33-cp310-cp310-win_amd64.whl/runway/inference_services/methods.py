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

from datetime import datetime
from typing import Optional, Dict, Any
from runway.inference_services.schemas import OwnerData, TagData
from runway.inference_services.models import InferenceService
from runway.inference_services.api_client import fetch_inference_services
from runway.inference_services.values import InferenceServiceLoggerType
from runway.common.values import DatabaseType
from runway.inference_services.schemas import (
    LoggerConnectionDatabaseConfig,
    Logger,
    Serving,
)

def _create_inference_service_instance(inference_service_data: Dict[str, Any]) -> InferenceService:
    """Create appropriate inference service instance from API response data

    Parameters
    ----------
    inference_service_data : Dict[str, Any]
        Raw service data from API response

    Returns
    -------
    InferenceService
        created inference service instance

    Raises
    ------
    NotImplementedError
        If logging storage type is not implemented in sdk
    """
    # Parse servings data with nested loggers
    servings = []

    for serving_data in inference_service_data["servings"]:

        loggers = []
        for logger in serving_data.get("loggers", []):
            storage_type = logger["storage"]["type"]

            if storage_type in [ db_type for db_type in DatabaseType]:
                connection_config = LoggerConnectionDatabaseConfig(**logger["storage"])
            else:
                raise NotImplementedError(f"Logger storage type {storage_type} is not supported yet")

            logger = Logger(
                id=logger["id"],
                type=InferenceServiceLoggerType(logger["type"]),
                connection_config=connection_config,
            )

            loggers.append(logger)

        serving = Serving(
            id=serving_data["id"],
            enable_logger=serving_data["enable_logger"],
            loggers=loggers,
        )
        servings.append(serving)


    # Common service parameters
    service_params = {
        "id": inference_service_data["id"],
        "name": inference_service_data["name"],
        "description": inference_service_data.get("description"),
        "created_at": datetime.fromtimestamp(inference_service_data["created_at"]),
        "updated_at": datetime.fromtimestamp(inference_service_data["updated_at"]),
        "owner": OwnerData(**inference_service_data["owner"]),
        "favorited": inference_service_data["favorited"],
        "tags": [TagData(**tag) for tag in inference_service_data["tags"]],
    }
    service = InferenceService(**service_params)
    service._servings = servings

    return service


def get_inference_services() -> Dict[str, InferenceService]:
    """Get all inference services

    Returns
    -------
    Dict[str, InferenceService]
        Dictionary of inference service objects keyed by service name.
    """
    response_data = fetch_inference_services()
    if response_data is None:
        return {}

    services = {}
    for service_data in response_data:
        service = _create_inference_service_instance(service_data)
        services[service.name] = service

    return services

def get_inference_service(name: str) -> Optional[InferenceService]:
    """Get specific inference service by name

    Parameters
    ----------
    name : str
        Name of the service to find

    Returns
    -------
    Optional[BaseInferenceService]
        Inference service object if found, None otherwise
    """
    services_data = fetch_inference_services(name)
    if not services_data:
        return None

    return _create_inference_service_instance(services_data[0])
