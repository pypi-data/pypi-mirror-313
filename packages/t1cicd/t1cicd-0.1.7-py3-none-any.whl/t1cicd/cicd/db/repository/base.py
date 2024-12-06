"""
This module contains the base repository class for the database models.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from psycopg_pool import AsyncConnectionPool

T = TypeVar("T")
CreateT = TypeVar("CreateT")


class BaseRepository(ABC, Generic[T, CreateT]):
    """This is the base repository class for the database models"""

    def __init__(self, pool: AsyncConnectionPool):
        self.pool = pool

    @abstractmethod
    async def create(self, item: CreateT) -> T:
        """
        Create a new item in the database.

        Args:
            item (CreateT): The item to create.

        Returns:
            T: The created item.
        """

    @abstractmethod
    async def get(self, id: UUID) -> T | None:
        """
        Get an item from the database.

        Args:
            id (UUID): The unique identifier for the item.

        Returns:
            T | None: The item if found, otherwise None.

        """

    @abstractmethod
    async def update(self, item: T) -> T | None:
        """
        Update an item in the database.

        Args:
            item (T): The item to update.

        Returns:
            T | None: The updated item if found, otherwise


        """

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete an item from the database.

        Args:
            id (UUID): The unique identifier for the item.

        Returns:
            bool: True if the item was deleted, otherwise False.
        """
