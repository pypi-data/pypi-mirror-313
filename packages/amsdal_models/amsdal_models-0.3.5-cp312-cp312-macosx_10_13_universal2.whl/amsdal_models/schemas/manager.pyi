from _typeshed import Incomplete
from amsdal_models.errors import AmsdalValidationError as AmsdalValidationError
from amsdal_models.schemas.data_models.schemas_directory import SchemasDirectory as SchemasDirectory
from amsdal_models.schemas.extenders.custom_code_extender import CustomCodeExtender as CustomCodeExtender
from amsdal_models.schemas.extenders.options_extender import OptionsExtender as OptionsExtender
from amsdal_models.schemas.loaders.cli_custom_code_loader import CliCustomCodeLoader as CliCustomCodeLoader
from amsdal_models.schemas.loaders.cli_loader import CliConfigLoader as CliConfigLoader
from amsdal_models.schemas.loaders.cli_options_loader import CliOptionsLoader as CliOptionsLoader
from amsdal_models.schemas.mixins.check_dependencies_mixin import CheckDependenciesMixin as CheckDependenciesMixin
from amsdal_models.schemas.mixins.enrich_schemas_mixin import EnrichSchemasMixin as EnrichSchemasMixin
from amsdal_models.schemas.mixins.verify_schemas_mixin import VerifySchemasMixin as VerifySchemasMixin
from amsdal_utils.models.data_models.schema import ObjectSchema
from collections.abc import Iterator
from pathlib import Path

logger: Incomplete

class BuildSchemasManager(EnrichSchemasMixin, VerifySchemasMixin, CheckDependenciesMixin):
    """
    Manages the building and verification of schemas.

    This class is responsible for loading, enriching, verifying, and checking dependencies of various schemas.
    It handles type, core, contrib, and user schemas, ensuring they are properly loaded and validated.
    """
    _type_schemas: list[ObjectSchema]
    _core_schemas: list[ObjectSchema]
    _contrib_schemas: list[ObjectSchema]
    _user_schemas: list[ObjectSchema]
    _schemas_directories: Incomplete
    def __init__(self, schemas_directories: list[SchemasDirectory]) -> None: ...
    @property
    def type_schemas(self) -> list[ObjectSchema]:
        """
        Retrieves the list of type schemas.

        This property method loads the type schemas if they are not already loaded and returns them.

        Returns:
            list[ObjectSchema]: A list of type schemas.
        """
    @property
    def core_schemas(self) -> list[ObjectSchema]:
        """
        Retrieves the list of core schemas.

        This property method loads the core schemas if they are not already loaded and returns them.

        Returns:
            list[ObjectSchema]: A list of core schemas.
        """
    @property
    def contrib_schemas(self) -> list[ObjectSchema]:
        """
        Retrieves the list of contrib schemas.

        This property method loads the contrib schemas if they are not already loaded and returns them.

        Returns:
            list[ObjectSchema]: A list of contrib schemas.
        """
    @property
    def user_schemas(self) -> list[ObjectSchema]:
        """
        Retrieves the list of user schemas.

        This property method loads the user schemas if they are not already loaded and returns them.

        Returns:
            list[ObjectSchema]: A list of user schemas.
        """
    def verify(self) -> None:
        """
        Loads and verifies all schemas.

        This method ensures that all schemas (type, core, contrib, and user schemas) are loaded and verified.

        Returns:
            None
        """
    def _load_schemas(self) -> None: ...
    @staticmethod
    def load_schemas_from_path(schemas_path: Path) -> Iterator[ObjectSchema]:
        """
        Loads schemas from the specified path.

        This method reads schemas from the given path and returns an iterator of `ObjectSchema` objects. It uses various
        loaders and extenders to process the schemas.

        Args:
            schemas_path (Path): The path from which to load the schemas.

        Returns:
            Iterator[ObjectSchema]: An iterator of `ObjectSchema` objects.
        """
    def dump_schemas(self, target_dir: Path) -> None:
        """
        Dumps all schemas to the specified directory.

        This method creates the target directory if it does not exist and writes the type, core, contrib,
            and user schemas to separate JSON files within the directory.

        Args:
            target_dir (Path): The directory where the schemas will be dumped.

        Returns:
            None
        """
    @staticmethod
    def _dump_schemas(target_file: Path, schemas: list[ObjectSchema]) -> None: ...
    @classmethod
    def add_user_schema(cls, target_dir: Path, object_schema: ObjectSchema) -> None:
        """
        Adds a user schema to the specified directory.

        This method adds the given `ObjectSchema` to the `user_schemas.json` file in the target directory. If the file
        already exists, it updates the existing schemas by removing any schema with the same title as the new schema
        before adding the new schema.

        Args:
            target_dir (Path): The directory where the user schema will be added.
            object_schema (ObjectSchema): The `ObjectSchema` object to add.

        Returns:
            None
        """

class SchemaManagerHandler:
    """
    Handles schema management operations.

    This class is responsible for loading, invalidating, and providing access to various schemas (type, core, contrib,
        and user schemas) from a specified directory.
    """
    _type_schemas: list[ObjectSchema]
    _core_schemas: list[ObjectSchema]
    _contrib_schemas: list[ObjectSchema]
    _user_schemas: list[ObjectSchema]
    _schemas_directory: Incomplete
    def __init__(self, schemas_directory: Path) -> None: ...
    def invalidate_user_schemas(self) -> None:
        """
        Invalidates the cached user schemas.

        This method removes the cached user schemas, forcing them to be reloaded the next time they are accessed.

        Returns:
            None
        """
    @property
    def type_schemas(self) -> list[ObjectSchema]:
        """
        Retrieves the list of type schemas.

        This property method loads the type schemas if they are not already loaded and returns them.

        Returns:
            list[ObjectSchema]: A list of type schemas.
        """
    @property
    def core_schemas(self) -> list[ObjectSchema]:
        """
        Retrieves the list of core schemas.

        This property method loads the core schemas if they are not already loaded and returns them.

        Returns:
            list[ObjectSchema]: A list of core schemas.
        """
    @property
    def contrib_schemas(self) -> list[ObjectSchema]:
        """
        Retrieves the list of contrib schemas.

        This property method loads the contrib schemas if they are not already loaded and returns them.

        Returns:
            list[ObjectSchema]: A list of contrib schemas.
        """
    @property
    def user_schemas(self) -> list[ObjectSchema]:
        """
        Retrieves the list of user schemas.

        This property method loads the user schemas if they are not already loaded and returns them.

        Returns:
            list[ObjectSchema]: A list of user schemas.
        """
    @property
    def all_schemas(self) -> list[ObjectSchema]:
        """
        Retrieves the list of all schemas.

        This property method combines and returns the type, core, contrib, and user schemas.

        Returns:
            list[ObjectSchema]: A list of all schemas, including type, core, contrib, and user schemas.
        """
    def _load_schemas(self) -> None: ...
    def _load_schema(self, schema_file: Path) -> list[ObjectSchema]: ...
