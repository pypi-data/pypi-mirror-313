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

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple, Union, List, Type

from runway.inference_services.schemas import (
    InferenceDatabaseRecordsFilter,
    InferenceDatabaseRecordsSorting,
)
from runway.common.schemas import DatabaseType
from runway.inference_services.schemas import InferenceDatabaseRecordsMatchType

class DBQueryBuilder(ABC):
    """Abstract base class for database-specific query builders"""

    def __init__(self) -> None:
        self.identifier_quote = '"'  # default to PostgreSQL style
        self.supports_limit_offset = True
        self.use_ilike = False

    def validate_custom_query(self, query: str) -> bool:
        """Validate if custom query is safe to execute

        Parameters
        ----------
        query : str
            Custom SQL query to validate

        Returns
        -------
        bool
            True if query is safe, False otherwise
        """
        query_upper = query.upper()

        # 식별자 인용 부호 균형 체크
        if self.identifier_quote:
            if query.count(self.identifier_quote) % 2 != 0:
                return False

        return True

    def build_select_query(
        self,
        table: str,
        sorting: Optional[Union[InferenceDatabaseRecordsSorting, List[InferenceDatabaseRecordsSorting]]] = None,
        filters: Optional[List[InferenceDatabaseRecordsFilter]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Tuple[str, Dict[str, Any]]:
        """Common query building logic for all RDBs"""
        query = f"SELECT * FROM {self.quote_identifier(table)}"
        params: Dict[str, Any] = {}

        # Filters
        if filters:
            conditions = []
            for filter in filters:
                param_name = f"filter_value_{len(params)}"
                params[param_name] = filter.match_value

                if filter.match_type == InferenceDatabaseRecordsMatchType.like:
                    params[param_name] = f"%{filter.match_value}%"
                    like_operator = "ILIKE" if self.use_ilike else "LIKE"
                    conditions.append(
                        f"{self.quote_identifier(filter.column_name)} {like_operator} :{param_name}",
                    )
                else:
                    conditions.append(
                        f"{self.quote_identifier(filter.column_name)} {self.get_operator(filter.match_type)} :{param_name}",
                    )

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

        # Sorting
        sorting_list = [sorting] if isinstance(sorting, InferenceDatabaseRecordsSorting) else sorting
        if sorting_list:
            order_clauses = [
                f"{self.quote_identifier(sort.column_name)} {sort.order_type.value}"
                for sort in sorting_list
            ]
            query += " ORDER BY " + ", ".join(order_clauses)

        # Pagination
        query = self.add_pagination(query, limit, offset)

        return query, params

    @abstractmethod
    def build_schema_query(self, table_name: str) -> str:
        """Build query to fetch table schema information"""
        raise NotImplementedError("Subclass must implement build_schema_query")

    def quote_identifier(self, identifier: str) -> str:
        """Quote database identifiers"""
        return f"{self.identifier_quote}{identifier}{self.identifier_quote}"

    def get_operator(self, match_type: InferenceDatabaseRecordsMatchType) -> str:
        """Get comparison operator"""
        return {
            InferenceDatabaseRecordsMatchType.eq: "=",
            InferenceDatabaseRecordsMatchType.ne: "!=",
            InferenceDatabaseRecordsMatchType.gt: ">",
            InferenceDatabaseRecordsMatchType.lt: "<",
            InferenceDatabaseRecordsMatchType.gte: ">=",
            InferenceDatabaseRecordsMatchType.lte: "<=",
            InferenceDatabaseRecordsMatchType.like: "LIKE",
        }[match_type]

    def add_pagination(self, query: str, limit: Optional[int], offset: Optional[int]) -> str:
        """Add pagination clauses"""
        if not self.supports_limit_offset:
            return query
        if limit is not None:
            query += f" LIMIT {limit}"
        if offset is not None:
            query += f" OFFSET {offset}"
        return query

class PostgreSQLQueryBuilder(DBQueryBuilder):
    def __init__(self) -> None:
        super().__init__()
        self.use_ilike = True  # PostgreSQL specific

    def validate_custom_query(self, query: str) -> bool:
        """PostgreSQL specific query validation

        Additional checks:
        - Balanced quotes
        - No function creation
        - No copy commands
        """
        if not super().validate_custom_query(query):
            return False

        query_upper = query.upper()

        # PostgreSQL identifier quotes should be balanced
        if query.count('"') % 2 != 0:
            return False

        return True


    def build_schema_query(self, table_name: str) -> str:
        return f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position
        """

class MySQLQueryBuilder(DBQueryBuilder):
    def __init__(self) -> None:
        super().__init__()
        self.identifier_quote = "`"

    def validate_custom_query(self, query: str) -> bool:
        """MySQL specific query validation"""
        if not super().validate_custom_query(query):
            return False

        query_upper = query.upper()

        # MySQL backticks should be balanced
        if query.count('`') % 2 != 0:
            return False

        return True

    def build_schema_query(self, table_name: str) -> str:
        return f"""
            SELECT column_name, data_type,
                   IF(is_nullable = 'YES', 'true', 'false') as is_nullable
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position
        """

class MSSQLQueryBuilder(DBQueryBuilder):
    def __init__(self) -> None:
        super().__init__()
        self.identifier_quote = "["

    def validate_custom_query(self, query: str) -> bool:
        """MSSQL specific query validation"""
        if not super().validate_custom_query(query):
            return False

        query_upper = query.upper()

        # MSSQL brackets should be balanced
        if query.count('[') != query.count(']'):
            return False

        return True

    def build_schema_query(self, table_name: str) -> str:
        return f"""
            SELECT column_name,
                   data_type,
                   DECODE(nullable, 'Y', 'true', 'false') as is_nullable
            FROM all_tab_columns
            WHERE table_name = UPPER('{table_name}')
            ORDER BY column_id
        """

    def add_pagination(self, query: str, limit: Optional[int], offset: Optional[int]) -> str:
        if offset is not None:
            query += f" OFFSET {offset} ROWS"
        if limit is not None:
            query += f" FETCH NEXT {limit} ROWS ONLY"
        return query

class OracleQueryBuilder(DBQueryBuilder):
    def __init__(self) -> None:
        super().__init__()
        self.identifier_quote = ""  # Oracle typically doesn't quote identifiers
        self.supports_limit_offset = False

    def validate_custom_query(self, query: str) -> bool:
        """Oracle specific query validation"""
        if not super().validate_custom_query(query):
            return False

        query_upper = query.upper()
        return True

    def build_schema_query(self, table_name: str) -> str:
        """Build query to fetch table schema information for Oracle

        Parameters
        ----------
        table_name : str
            Name of the table to get schema for

        Returns
        -------
        str
            SQL query to fetch schema information
        """
        return f"""
            SELECT
                column_name,
                data_type,
                CASE
                    WHEN nullable = 'Y' THEN 'true'
                    ELSE 'false'
                END as is_nullable
            FROM all_tab_columns
            WHERE table_name = UPPER('{table_name}')
            ORDER BY column_id
        """

    def add_pagination(self, query: str, limit: Optional[int], offset: Optional[int]) -> str:
        if offset is not None and limit is not None:
            return f"""
                SELECT * FROM (
                    SELECT a.*, ROWNUM rnum FROM (
                        {query}
                    ) a WHERE ROWNUM <= {offset + limit}
                ) WHERE rnum > {offset}
            """
        return query

class TiberoQueryBuilder(OracleQueryBuilder):
    """Tibero uses Oracle-compatible syntax"""
    pass

# Add other DB-specific builders as needed
ConcreteQueryBuilder = Union[PostgreSQLQueryBuilder, MySQLQueryBuilder, OracleQueryBuilder, MSSQLQueryBuilder, TiberoQueryBuilder]
BuilderType = Type[ConcreteQueryBuilder]

class DBQueryBuilderFactory:
    """Factory for creating database-specific query builders"""

    _builders: Dict[DatabaseType, BuilderType] = {
        DatabaseType.postgresql: PostgreSQLQueryBuilder,
        DatabaseType.mysql: MySQLQueryBuilder,
        DatabaseType.oracle: OracleQueryBuilder,
        DatabaseType.mssql: MSSQLQueryBuilder,
        DatabaseType.tibero: TiberoQueryBuilder,
    }

    ConcreteQueryBuilder = Union[PostgreSQLQueryBuilder, MySQLQueryBuilder, OracleQueryBuilder, MSSQLQueryBuilder, TiberoQueryBuilder]


    @classmethod
    def get_builder(cls, db_type: DatabaseType) -> ConcreteQueryBuilder:
        builder_class = cls._builders.get(db_type)
        if not builder_class:
            raise ValueError(f"Unsupported database type: {db_type}")
        return builder_class()
