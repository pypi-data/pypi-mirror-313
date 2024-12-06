from _typeshed import Incomplete
from amsdal_models.classes.base import BaseModel as BaseModel
from amsdal_models.classes.errors import AmsdalClassError as AmsdalClassError, AmsdalClassNotFoundError as AmsdalClassNotFoundError
from amsdal_models.classes.model import Model as Model
from amsdal_models.classes.utils import resolve_modes_module as resolve_modes_module
from amsdal_models.classes.writer import ClassWriter as ClassWriter
from amsdal_models.schemas.data_models.schemas_directory import SchemasDirectory as SchemasDirectory
from amsdal_utils.models.enums import SchemaTypes as SchemaTypes
from amsdal_utils.models.mixins.cached_mixin import CachedMixin
from amsdal_utils.utils.singleton import Singleton
from pathlib import Path

class ClassManager(CachedMixin, metaclass=Singleton):
    """
    Manages the lifecycle and operations of model classes.

    Attributes:
        models_dir (Path): The directory where models are stored.
    """
    models_dir: Path
    _loaded_classes: Incomplete
    def __init__(self) -> None: ...
    def init_models_root(self, models_dir: Path) -> None:
        """
        Initializes the root directory for models.

        Args:
            models_dir (Path): The directory where models are stored.
        """
    @property
    def models_module_name(self) -> str:
        """
        Returns the name of the model's module.

        Returns:
            str: The name of the model's module.
        """
    def init_sys_path(self) -> None:
        """
        Initializes the system path for importing models.

        This method ensures that the necessary directories are created and added to the system path
        to allow for the importing of model classes.

        Raises:
            OSError: If there is an error creating the directories or touching the `__init__.py` file.
        """
    def generate_models(self, schemas_dirs: list[SchemasDirectory]) -> None:
        """
        Generates models from schema directories.

        Args:
            schemas_dirs (list[SchemasDirectory]): A list of schema directories to generate models from.

        Returns:
            None
        """
    def teardown(self) -> None:
        """
        Tears down the model manager by unloading all classes and removing the model directory from the system path.

        This method ensures that all loaded classes are unloaded, the model directory is removed from the system path,
        and the class cache is invalidated.
        """
    def resolve_schema_type(self, class_name: str) -> SchemaTypes:
        """
        Resolves the schema type for a given class name.

        Args:
            class_name (str): The name of the class to resolve the schema type for.

        Returns:
            SchemaTypes: The resolved schema type.

        Raises:
            AmsdalClassError: If the class name is not found in the loaded classes.
        """
    def import_model_class(self, class_name: str, schema_type: SchemaTypes) -> type['Model']:
        """
        Imports a model class for a given class name and schema type.

        Args:
            class_name (str): The name of the class to import.
            schema_type (SchemaTypes): The schema type of the class to import.

        Returns:
            type[Model]: The imported model class.

        Raises:
            AmsdalClassError: If the imported class is not a subclass of Model.
        """
    def import_class(self, class_name: str, schema_type: SchemaTypes) -> type[BaseModel]:
        """
        Imports a class for a given class name and schema type.

        Args:
            class_name (str): The name of the class to import.
            schema_type (SchemaTypes): The schema type of the class to import.

        Returns:
            type[BaseModel]: The imported class.

        Raises:
            AmsdalClassNotFoundError: If the class cannot be found in the specified module.
        """
    def unload_classes(self, class_name: str, schema_type: SchemaTypes) -> None:
        """
        Unloads a class for a given class name and schema type.

        Args:
            class_name (str): The name of the class to unload.
            schema_type (SchemaTypes): The schema type of the class to unload.

        Returns:
            None
        """
    def unload_all_classes(self) -> None:
        """
        Unloads all loaded classes.

        This method iterates through all loaded classes and unloads them by calling the `unload_classes` method
        for each class name and schema type.
        """
