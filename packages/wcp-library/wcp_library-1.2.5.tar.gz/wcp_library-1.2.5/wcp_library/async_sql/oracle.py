import logging
from typing import Optional

import numpy as np
import pandas as pd
import oracledb
from oracledb import AsyncConnectionPool

from wcp_library.async_sql import retry

logger = logging.getLogger(__name__)


async def _connect_warehouse(username: str, password: str, hostname: str, port: int, database: str, min_connections: int,
                             max_connections: int) -> AsyncConnectionPool:
    """
    Create Warehouse Connection

    :param username: username
    :param password: password
    :param hostname: hostname
    :param port: port
    :param database: database
    :param min_connections:
    :param max_connections:
    :return: session_pool
    """

    dsn = oracledb.makedsn(hostname, port, sid=database)
    session_pool = oracledb.create_pool_async(
        user=username,
        password=password,
        dsn=dsn,
        min=min_connections,
        max=max_connections,
        increment=1
    )
    return session_pool


class AsyncOracleConnection(object):
    """
    SQL Connection Class

    :return: None
    """

    def __init__(self, min_connections: int = 2, max_connections: int = 5):
        self._db_service: str = "Oracle"
        self._username: Optional[str] = None
        self._password: Optional[str] = None
        self._hostname: Optional[str] = None
        self._port: Optional[int] = None
        self._database: Optional[str] = None
        self._sid: Optional[str] = None
        self._session_pool: Optional[AsyncConnectionPool] = None

        self.min_connections = min_connections
        self.max_connections = max_connections

        self._retry_count = 0
        self.retry_limit = 50
        self.retry_error_codes = ['ORA-01033', 'DPY-6005', 'DPY-4011']

    @retry
    async def _connect(self) -> None:
        """
        Connect to the warehouse

        :return: None
        """

        sid_or_service = self._database if self._database else self._sid

        self._session_pool = await _connect_warehouse(self._username, self._password, self._hostname, self._port,
                                                      sid_or_service, self.min_connections, self.max_connections)

    async def set_user(self, credentials_dict: dict) -> None:
        """
        Set the user credentials and connect

        :param credentials_dict: dictionary of connection details
        :return: None
        """

        if not ([credentials_dict['Service'] or credentials_dict['SID']]):
            raise ValueError("Either Service or SID must be provided")

        self._username: Optional[str] = credentials_dict['UserName']
        self._password: Optional[str] = credentials_dict['Password']
        self._hostname: Optional[str] = credentials_dict['Host']
        self._port: Optional[int] = int(credentials_dict['Port'])
        self._database: Optional[str] = credentials_dict['Service'] if 'Service' in credentials_dict else None
        self._sid: Optional[str] = credentials_dict['SID'] if 'SID' in credentials_dict else None

        await self._connect()

    async def close_connection(self) -> None:
        """
        Close the connection

        :return: None
        """

        await self._session_pool.close()

    @retry
    async def execute(self, query: str) -> None:
        """
        Execute the query

        :param query: query
        :return: None
        """

        async with self._session_pool.acquire() as connection:
            with connection.cursor() as cursor:
                await cursor.execute(query)
                await connection.commit()

    @retry
    async def safe_execute(self, query: str, packed_values: dict) -> None:
        """
        Execute the query without SQL Injection possibility, to be used with external facing projects.

        :param query: query
        :param packed_values: dictionary of values
        :return: None
        """

        async with self._session_pool.acquire() as connection:
            with connection.cursor() as cursor:
                await cursor.execute(query, packed_values)
                await connection.commit()

    @retry
    async def execute_multiple(self, queries: list[list[str, dict]]) -> None:
        """
        Execute multiple queries

        :param queries: list of queries
        :return: None
        """

        async with self._session_pool.acquire() as connection:
            with connection.cursor() as cursor:
                for item in queries:
                    query = item[0]
                    packed_values = item[1]
                    if packed_values:
                        await cursor.execute(query, packed_values)
                    else:
                        await cursor.execute(query)
                await connection.commit()

    @retry
    async def execute_many(self, query: str, dictionary: list[dict]) -> None:
        """
        Execute many queries

        :param query: query
        :param dictionary: dictionary of values
        :return: None
        """

        async with self._session_pool.acquire() as connection:
            with connection.cursor() as cursor:
                await cursor.executemany(query, dictionary)
                await connection.commit()

    @retry
    async def fetch_data(self, query: str, packed_data=None):
        """
        Fetch the data from the query

        :param query: query
        :param packed_data: packed data
        :return: rows
        """

        async with self._session_pool.acquire() as connection:
            with connection.cursor() as cursor:
                if packed_data:
                    await cursor.execute(query, packed_data)
                else:
                    await cursor.execute(query)
                rows = await cursor.fetchall()
        return rows

    @retry
    async def export_DF_to_warehouse(self, dfObj: pd.DataFrame, outputTableName: str, columns: list, remove_nan=False) -> None:
        """
        Export the DataFrame to the warehouse

        :param dfObj: DataFrame
        :param outputTableName: output table name
        :param columns: list of columns
        :param remove_nan: remove NaN values
        :return: None
        """

        col = ', '.join(columns)
        bindList = []
        for column in columns:
            bindList.append(':' + column)
        bind = ', '.join(bindList)

        if remove_nan:
            dfObj = dfObj.replace({np.nan: None})
        main_dict = dfObj.to_dict('records')

        # if remove_nan:
        #     for val, item in enumerate(main_dict):
        #         for sub_item, value in item.items():
        #             if pd.isna(value):
        #                 main_dict[val][sub_item] = None
        #             else:
        #                 main_dict[val][sub_item] = value

        query = """INSERT INTO {} ({}) VALUES ({})""".format(outputTableName, col, bind)
        await self.execute_many(query, main_dict)

    @retry
    async def truncate_table(self, tableName: str) -> None:
        """
        Truncate the table

        :param tableName: table name
        :return: None
        """

        truncateQuery = """TRUNCATE TABLE {}""".format(tableName)
        await self.execute(truncateQuery)

    @retry
    async def empty_table(self, tableName: str) -> None:
        """
        Empty the table

        :param tableName: table name
        :return: None
        """

        deleteQuery = """DELETE FROM {}""".format(tableName)
        await self.execute(deleteQuery)
