"""
This module contains the database initialization and management functions.
"""

import asyncio
from pathlib import Path
from typing import Type, TypeVar

from flask import Flask
from psycopg_pool import AsyncConnectionPool

from t1cicd.cicd.db.config import DBConfig
from t1cicd.cicd.db.repository.base import BaseRepository
from t1cicd.cicd.db.transaction.base import BaseTransaction
from t1cicd.cicd.db.utils.db_initializer import DBInitializer

T = TypeVar("T")
TTransaction = TypeVar("TTransaction", bound="BaseTransaction")


class DB:
    """
    Database class for managing the connection pool and repositories.
    """

    _pool: AsyncConnectionPool | None = None
    """The connection pool"""
    _repositories: dict[str, BaseRepository] = {}
    """The repository instances"""
    _transactions: dict[str, BaseTransaction] = {}
    """The transaction instances"""

    @classmethod
    async def init(cls, config: DBConfig):
        """
        DB initialization, open the connection pool

        Args:
            config (DBConfig): The database configuration


        """
        if cls._pool is None:
            pool = AsyncConnectionPool(
                min_size=config.min_size,
                max_size=config.max_size,
                conninfo=config.conninfo,
                open=False,
            )
            await pool.open()
            cls._pool = pool
            cls._repositories = {}
            cls._transactions = {}

    @classmethod
    async def close(cls):
        """
        Close the connection pool
        """
        if cls._pool:
            await cls._pool.close()
            cls._pool = None
            cls._repositories = {}
            cls._transactions = {}

    @classmethod
    def get_pool(cls) -> AsyncConnectionPool:
        """
        Get the connection pool
        """
        if cls._pool is None:
            raise ValueError("DB not initialized")
        return cls._pool

    @classmethod
    def get_repository(cls, repo_class: Type[T]) -> T:
        """
        Get the repository instance

        Args:
            repo_class (Type[T]): The repository class

        Returns:
            T: The repository instance
        """
        repo_name = repo_class.__name__
        if repo_name not in cls._repositories:
            cls._repositories[repo_name] = repo_class(cls.get_pool())
        return cls._repositories[repo_name]

    @classmethod
    def get_transaction(cls, transaction_class: Type[TTransaction]) -> TTransaction:
        """

        Get the transaction instance

        Args:
            transaction_class (Type[TTransaction]): The transaction class

        Returns:
            TTransaction: The transaction instance
        """
        transaction_name = transaction_class.__name__
        if transaction_name not in cls._transactions:
            cls._transactions[transaction_name] = transaction_class(cls.get_pool())
        return cls._transactions[transaction_name]


def init_flask_db(app: Flask):
    """
    Initialize the database for the Flask app
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def _async_init():
        config = DBConfig.from_env()
        await DBInitializer.ensure_database_exists(config)
        await DB.init(config)
        async with DB.get_pool().connection() as conn:
            # check if tables exist
            if not await DBInitializer.check_tables_exist(conn):
                migration_dir = Path(__file__).parent / "migration"

                await DBInitializer.execute_migration_files(conn, str(migration_dir))
        try:
            async with DB.get_pool().connection() as conn:
                await conn.execute("SELECT 1")
                app.logger.info("Database connection successful")
        except Exception as e:
            app.logger.error(f"Database connection failed: {e}")
            raise

    try:
        loop.run_until_complete(_async_init())
    finally:
        loop.close()
