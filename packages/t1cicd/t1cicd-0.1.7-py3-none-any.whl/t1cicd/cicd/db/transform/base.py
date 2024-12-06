"""
This module defines the ModelRelationship class, which is used to manage
relationships between Pydantic models and replace IDs with objects.
"""

from typing import Optional, Type

from pydantic import BaseModel
from typing_extensions import Generic, TypeVar

T = TypeVar("T", bound=BaseModel)
R = TypeVar("R", bound=BaseModel)


class ModelRelationship(Generic[T, R]):
    """
    A class to manage relationships between Pydantic models and replace IDs with objects.

    Attributes:
        parent_model (Type[T]): The parent model class.
        related_model (Type[R]): The related model class.
        related_ids_field (str): The field name in the parent model that contains related IDs.
        nested_relationship (Optional[ModelRelationship]): An optional nested relationship.
    """

    def __init__(
        self,
        parent_model: Type[T],
        related_model: Type[R],
        related_ids_field: str,
        nested_relationship: Optional["ModelRelationship"] = None,
    ):
        """
        Initializes the ModelRelationship instance.

        Args:
            parent_model (Type[T]): The parent model class.
            related_model (Type[R]): The related model class.
            related_ids_field (str): The field name in the parent model that contains related IDs.
            nested_relationship (Optional[ModelRelationship]): An optional nested relationship.
        """
        self.parent_model = parent_model
        self.related_model = related_model
        self.related_ids_field = related_ids_field
        self.nested_relationship = nested_relationship

    def replace_ids_with_objects(
        self,
        parent: T,
        related_objects: list[R],
        next_level_objects: list | None = None,
    ) -> dict:
        """
        Replace the related ids in the parent object with the related objects.

        Args:
            parent (T): The parent object.
            related_objects (list[R]): The related objects.
            next_level_objects (list | None): The next level related objects.

        Returns:
            dict: The parent object with the related objects
        """
        result = parent.model_dump()
        objects_map = {obj.id: obj for obj in related_objects}

        nest_field_name = self.related_model.__name__.lower()

        related_ids = result.pop(self.related_ids_field)

        nested_objects = []
        for _id in related_ids:
            if _id in objects_map:
                obj = objects_map[_id]
                if self.nested_relationship and next_level_objects:
                    nested_objects.append(
                        self.nested_relationship.replace_ids_with_objects(
                            obj, next_level_objects
                        )
                    )
                else:
                    nested_objects.append(obj.model_dump())

        result[nest_field_name] = nested_objects
        return result
