import logging
from contextlib import asynccontextmanager
from typing import Optional

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from pyback.pgsql.pg_config import PGConfig
from pyback.pgsql.pg_credentials import PGCredentials


class PGSQLAsyncClient:
    def __init__(
        self,
        credentials: PGCredentials,
        config: Optional[PGConfig] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self._credentials = credentials
        self._config = config or PGConfig()
        self.logger = logger or logging.getLogger(__name__)
        self.pool = self._create_pool()

    @asynccontextmanager
    async def connect(self):
        conn = await self.pool.connect()
        try:
            yield conn
        finally:
            await conn.close()

    def _create_pool(self) -> AsyncEngine:
        self.logger.debug(f"Creating async engine: {self._config}")

        conn_str = sqlalchemy.engine.URL.create(
            drivername="async+postgresql+asyncpg",
            username=self._credentials.username,
            password=self._credentials.password,
            database=self._credentials.database,
            host=self._credentials.host,
            port=self._credentials.port,
        )

        pool = create_async_engine(url=conn_str, **self._config.to_dict())

        return pool
