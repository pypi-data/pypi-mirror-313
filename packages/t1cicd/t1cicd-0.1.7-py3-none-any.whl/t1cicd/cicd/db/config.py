"""
This module contains the configuration class for the database.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class DBConfig:
    """
    Configuration class for the database.
    """

    host: str
    """The host of the database"""
    port: int
    """The port of the database"""
    dbname: str
    """The name of the database"""
    user: str
    """The user of the database"""
    password: str
    """The password of the database"""
    min_size: int
    """The minimum size of the connection pool"""
    max_size: int
    """The maximum size of the connection pool"""

    @classmethod
    def from_env(cls) -> "DBConfig":
        """
        Create configuration from environment variables

        Returns:
            DBConfig: The configuration object
        """
        return cls(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            dbname=os.getenv("DB_NAME", "cs6510"),
            user=os.getenv("DB_USER", "postgresql"),
            password=os.getenv("DB_PASSWORD", ""),
            min_size=int(os.getenv("DB_POOL_MIN_SIZE", "1")),
            max_size=int(os.getenv("DB_POOL_MAX_SIZE", "5")),
        )

    @property
    def conninfo(self) -> str:
        """
        Get the connection info string

        Returns:
            str: The connection info string
        """
        return (
            f"host={self.host} port={self.port} dbname={self.dbname} user={self.user}"
        )
