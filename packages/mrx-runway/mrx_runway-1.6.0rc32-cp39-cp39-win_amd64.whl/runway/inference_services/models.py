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

import json
from pandas.errors import EmptyDataError
from typing_extensions import override
from pydantic import PrivateAttr
from abc import ABC, abstractmethod
from datetime import datetime
import pandas as pd
from typing import Optional, List, Dict, Any, Union
from runway.inference_services.schemas import (
	InferenceDatabaseRecordsQuery,
	OwnerData,
	TagData,
	Serving,
	LoggerConnectionDatabaseConfig,
)
from runway.inference_services.query_builders import DBQueryBuilderFactory
from runway.common.schemas import BasePydanticInfo, DatabaseConfig
from runway.common.database import DatabaseClient
from sqlalchemy import text
from runway.common.values import DatabaseType

class InferenceRecords(ABC, BasePydanticInfo):
    @abstractmethod
    def to_dataframe(self) -> pd.DataFrame:
        """Convert records to pandas DataFrame

        Returns
        -------
        pd.DataFrame
            DataFrame containing the query results
        """
        raise NotImplementedError

    @abstractmethod
    @override
    def to_dict(self) -> Dict[str, Any]:
        """Convert records to dictionary format

        Returns
        -------
        Dict[str, Any]
            Dictionary containing rows and schema information
        """
        raise NotImplementedError


class InferenceDatabaseRecords(InferenceRecords):
    """Inference service database records"""

    _rows: List[Any] = PrivateAttr(default=None)
    _records_schema: Optional[List[Dict[str, Any]]] = PrivateAttr(default=None)
    _is_select_query: bool = PrivateAttr(default=True)

    class Config:
        underscore_attrs_are_private = True
        allow_underscore_names = True

    def _get_column_names(self) -> List[str]:
        """Get column names from schema list

        Returns
        -------
        List[str]
            List of column names from the schema

        Raises
        ------
        ValueError
            If schema is not initialized
        """
        if not self._records_schema:
            raise ValueError(
                "Schema is not initialized. Make sure the storage logger is properly configured and accessible.",
            )

        try:
            return [col["column_name"] for col in self._records_schema]
        except ValueError as e:
            raise ValueError(f"Invalid schema format: missing {str(e)}") from e

    def to_dataframe(self) -> pd.DataFrame:
        """Convert records to pandas DataFrame

        Returns
        -------
        pd.DataFrame
            DataFrame containing the query results with proper column names

        Raises
        ------
        EmptyDataError
            If rows is empty
        """
        column_names = self._get_column_names()
        if not self._is_select_query:
            raise EmptyDataError
        return pd.DataFrame(self._rows, columns=column_names)

    def to_dict(self) -> Dict[str, Any]:
        """Convert records to dictionary format

        Overrides BasePydanticInfo.to_dict() to provide custom dictionary format

        Returns
        -------
        Dict[str, Any]
            Dictionary containing rows and schema information

        Raises
        ------
        EmptyDataError
            If rows is empty
        """
        if not self._is_select_query:
            raise EmptyDataError
        return {
            "result":[dict(zip(self._get_column_names(), row)) for row in self._rows],
        }


class InferenceService(BasePydanticInfo):
    """Represents an inference service

    This class manages inference service information and provides functionality
    to access and query inference records.

    Attributes
    ----------
    id : int
        Unique identifier for the service
    name : str
        Name of the service
    description : Optional[str]
        Description of the service
    created_at : datetime
        service creation time
    updated_at : datetime
        last service update time
    owner : OwnerData
        Owner information of the service
    favorited : bool
        Whether the service is marked as favorite
    tags : List[TagData]
        List of tags associated with the service
    """

    id : int
    name : str
    description : Optional[str]
    created_at : datetime
    updated_at : datetime
    owner : OwnerData
    favorited : bool
    tags : List[TagData]
    # Private fields using PrivateAttr
    _servings: List[Serving] = PrivateAttr(default=None)
    _db_connection: Optional[DatabaseClient] = PrivateAttr(default=None)
    _records_schema: str = PrivateAttr(default=None)

    class Config:
        underscore_attrs_are_private = True
        allow_underscore_names = True


    @property
    def _first_logger_connection_config(self) -> Optional[LoggerConnectionDatabaseConfig]:
        """Get first available logger connection config"""
        if not self._servings[0].loggers:
            return None

        logger = self._servings[0].loggers[0]
        if not isinstance(logger.connection_config, LoggerConnectionDatabaseConfig):
            raise NotImplementedError("Only DB logger connection config is supported")

        return LoggerConnectionDatabaseConfig(
                type=logger.connection_config.type,
                host=logger.connection_config.host,
                port=logger.connection_config.port,
                user=logger.connection_config.user,
                password=logger.connection_config.password,
                database=logger.connection_config.database,
                table=logger.connection_config.table,
        )



    def _get_logger_connection_config(
        self,
        logger_id: Optional[int] = None,
    ) -> Optional[Union[LoggerConnectionDatabaseConfig]]:
        """Get storage configuration for specific serving and logger IDs

        If neither serving_id nor logger_id is provided, returns the first available config.
        If IDs are provided but not found, falls back to the first available config.

        Parameters
        ----------
        logger_id : Optional[int]
            ID of the logger to find

        Returns
        -------
        Optional[Union[LoggerConnectionDatabaseConfig]]
            Storage configuration for the specified IDs or first available config

        Raises
        ------
        ValueError
            If no storage loggers exist or if specified IDs are not found
        """
        config = self._first_logger_connection_config
        if not config:
            return None

        if logger_id is None:
            logger_id = self._servings[0].loggers[0].id

        for serving in self._servings:
            for logger in serving.loggers:
                if logger.id == logger_id and not isinstance(logger.connection_config, LoggerConnectionDatabaseConfig):
                    raise NotImplementedError("Only DB logger connection config is supported")
                if logger_id and logger.id != logger_id:
                    continue

                return logger.connection_config

        return None


    def _get_db_logger_connection(self, logger_connection_config: LoggerConnectionDatabaseConfig) -> DatabaseClient:
        """Create or get database connection for the given database configuration

        Parameters
        ----------
        logger_connection_config : DBLoggingStorageConfig
            Storage configuration containing database connection details

        Returns
        -------
        DatabaseClient
            Database client instance for the specified configuration
        """

        config = DatabaseConfig(
            type=logger_connection_config.type,
            host=logger_connection_config.host,
            port=int(logger_connection_config.port),
            database=logger_connection_config.database,
            username=logger_connection_config.user,
            password=logger_connection_config.password,
        )

        self._db_connection = DatabaseClient(config)

        return self._db_connection

    #TODO:  add param logger_id: Optional[int] = None
    def get_inference_records_schema(self) -> str:
        """Get records schema lazily

        Returns
        -------
        Optional[str]
            Schema if available, None otherwise
        """

        connection_config = self._get_logger_connection_config()

        if isinstance(connection_config, LoggerConnectionDatabaseConfig):
            db = self._get_db_logger_connection(connection_config)

            try:
                db_type = DatabaseType(connection_config.type)
                query_builder = DBQueryBuilderFactory.get_builder(db_type)
                schema_query = query_builder.build_schema_query(connection_config.table)

                with db.get_session() as session:
                    result = session.execute(text(schema_query))
                    columns = [
                        {
                            "column_name": row.column_name,
                            "data_type": row.data_type,
                            "is_nullable": row.is_nullable,
                        }
                        for row in result
                    ]

                return json.dumps(columns)

            except ValueError as e:
                raise ValueError(
                    f"Failed to fetch schema for {connection_config.type} database: {str(e)}\n"
                    f"Table: {connection_config.table}",
                ) from e
        else:
            raise NotImplementedError("Only DB logger connection config is supported")


    def get_inference_records(
        self,
        query: Union[str, InferenceDatabaseRecordsQuery],
    ) -> Optional[Union[InferenceDatabaseRecords]]:
        """Get inference records from the service

        Parameters
        ----------
        query : Union[str, InferenceDatabaseRecordsQuery]
            custom query string or InferenceDatabaseRecordsQuery

        Returns
        -------
        Optional[Union[InferenceDatabaseRecords]]
            Inference records from the service
        """
        connection_config = self._get_logger_connection_config()
        if isinstance(connection_config, LoggerConnectionDatabaseConfig):
            db = self._get_db_logger_connection(connection_config)

            db_type = DatabaseType(connection_config.type)
            query_builder = DBQueryBuilderFactory.get_builder(db_type)

            params: Dict[str, Any] = {}

            if type(query) is str:
                # 사용자 정의 쿼리 검증
                if not query_builder.validate_custom_query(query):
                    raise ValueError(
                        f"query is not compatible with {db_type.value} database. "
                        "Please check the query syntax and database-specific features.",
                    )

            else:
                if type(query) is InferenceDatabaseRecordsQuery:
                    query, params = query_builder.build_select_query(
                        table=connection_config.table,
                        filters=query.filters,
                        sorting=query.sorting,
                        limit=query.limit,
                        offset=query.offset,
                    )

            with db.get_session() as session:
                try:
                    if type(query) is str:
                        result = session.execute(text(query), params)
                        rows = []
                        if result.returns_rows:
                            rows = [row for row in result]
                except ValueError as e:
                    raise ValueError(
                        f"Query execution failed for {db_type.value} database: {str(e)}\n"
                        f"Current database type: {db_type.value}\n"
                        f"Query: {query}\n"
                        "Please ensure your query is compatible with the target database.",
                    ) from e
            records_schema_str = self.get_inference_records_schema()
            records = InferenceDatabaseRecords()
            records._rows = rows
            records._records_schema = json.loads(records_schema_str)
            records._is_select_query = result.returns_rows
            return records

        else:
            raise NotImplementedError("Only DB logger connection config is supported")
