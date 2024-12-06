from amsdal_models.schemas.manager import BuildSchemasManager as BuildSchemasManager
from pydantic import BaseModel
from typing import Any

class DependencyModelNames(BaseModel):
    type_model_names: list[str]
    core_model_names: list[str]
    contrib_model_names: list[str]
    user_model_names: list[str]
    reference_model_names: list[str]
    @classmethod
    def build_from_schemas_manager(cls, schemas_manager: BuildSchemasManager) -> DependencyModelNames:
        """
        Builds DependencyModelNames from a schemas manager.

        Args:
            schemas_manager (BuildSchemasManager): The schemas manager.

        Returns:
            DependencyModelNames: The built DependencyModelNames instance.
        """
    @classmethod
    def build_from_database(cls) -> DependencyModelNames:
        """
        Builds DependencyModelNames from the database.

        Returns:
            DependencyModelNames: The built DependencyModelNames instance.
        """

class DependencyItem(BaseModel):
    module: tuple[str | None, str, str | None]
    def __eq__(self, other: Any) -> bool: ...
    def __hash__(self) -> int: ...
