"""
This module contains utility functions for initializing the database

"""

import os

import asyncpg

from t1cicd.cicd.db.config import DBConfig


class DBInitializer:
    """
    Utility class for initializing the database


    """

    @classmethod
    async def ensure_database_exists(cls, config: DBConfig) -> None:
        """
        Connect to postgres database and create the target database if it doesn't exist
        """
        # Connect to postgres database first
        postgres_conn = await asyncpg.connect(
            user=config.user,
            password=config.password,
            host=config.host,
            port=config.port,
            database="postgres",  # Connect to default postgres database
        )
        target_database = config.dbname

        try:
            # Check if our target database exists
            check_query = "SELECT 1 FROM pg_database WHERE datname = $1"
            exists = await postgres_conn.fetchval(check_query, target_database)

            if not exists:
                # Create the database if it doesn't exist
                print(f"Creating database {target_database}...")
                await postgres_conn.execute(f'CREATE DATABASE "{target_database}"')
                print(f"Database {target_database} created successfully")
            else:
                print(f"Database {target_database} already exists")

        finally:
            await postgres_conn.close()

    @classmethod
    async def check_tables_exist(cls, conn) -> bool:
        """
        Check if any tables exist in the database
        """
        async with conn.cursor() as cur:
            query = """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    AND table_type = 'BASE TABLE'
                );
            """
            result = await cur.execute(query)
            row = await result.fetchone()
            return row[0] if row else False

    @classmethod
    async def execute_migration_files(cls, conn, migration_dir: str) -> None:
        """
        Execute all SQL files in the migrations directory in sorted order using cursor
        """
        migration_files = sorted(
            [f for f in os.listdir(migration_dir) if f.endswith(".sql")]
        )

        async with conn.cursor() as cur:
            for file_name in migration_files:
                file_path = os.path.join(migration_dir, file_name)
                with open(file_path, "r", encoding="utf-8") as f:
                    sql = f.read()

                try:
                    await cur.execute(sql)
                    print(f"Successfully executed migration: {file_name}")
                except Exception as e:
                    print(f"Error executing migration {file_name}: {e}")
                    raise
