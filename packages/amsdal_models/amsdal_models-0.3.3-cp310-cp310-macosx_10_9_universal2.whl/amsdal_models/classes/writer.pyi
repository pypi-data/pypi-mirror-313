from _typeshed import Incomplete
from amsdal_models.classes.builder.class_source_builder import ClassSourceBuilder as ClassSourceBuilder
from amsdal_models.classes.constants import CONTRIB_MODELS_MODULE as CONTRIB_MODELS_MODULE, CORE_MODELS_MODULE as CORE_MODELS_MODULE, TYPE_MODELS_MODULE as TYPE_MODELS_MODULE, USER_MODELS_MODULE as USER_MODELS_MODULE
from amsdal_models.classes.data_models.dependencies import DependencyModelNames as DependencyModelNames
from amsdal_models.classes.model import Model as Model, TypeModel as TypeModel
from amsdal_models.classes.utils import resolve_base_class_for_schema as resolve_base_class_for_schema
from amsdal_models.schemas.data_models.schemas_directory import SchemasDirectory as SchemasDirectory
from amsdal_models.schemas.manager import BuildSchemasManager as BuildSchemasManager
from amsdal_utils.models.data_models.schema import ObjectSchema as ObjectSchema
from amsdal_utils.models.enums import SchemaTypes
from pathlib import Path

class ClassWriter:
    models_dir: Incomplete
    def __init__(self, models_dir: Path) -> None: ...
    @property
    def models_module_name(self) -> str:
        """
        Returns the name of the models module.

        This property retrieves the name of the directory where the models are stored.

        Returns:
            str: The name of the models module directory.
        """
    def generate_models(self, schemas_dirs: list[SchemasDirectory]) -> None:
        """
        Generate different types of models based on the provided schema directories.

        This method utilizes the provided schema directories to initialize a
        `BuildSchemasManager` and generates models in various categories, including
        type models, core models, contrib models, and user models. It also builds
        the dependency model names from the schema manager.

        Args:
            schemas_dirs (list[SchemasDirectory]): A list of schema directory objects
            used for building the schemas' manager.

        Returns:
            None
        """
    def generate_type_models(self, schemas_manager: BuildSchemasManager, model_names: DependencyModelNames) -> None:
        """
        Generate type-specific models based on the provided schemas.

        This method iterates through the type schemas from the `schemas_manager`
        and generates models for each schema that matches the required conditions.
        Specifically, it checks that the schema title matches the base class `OBJECT`.
        For each valid schema, it invokes the `generate_model` method with the
        appropriate parameters to create the model.

        Args:
            schemas_manager (BuildSchemasManager): An instance of the schema manager
            that holds the type schemas to be processed.

            model_names (DependencyModelNames): An instance containing the names of
            models used to handle dependencies between schemas.

        Returns:
            None
        """
    def generate_core_models(self, schemas_manager: BuildSchemasManager, model_names: DependencyModelNames) -> None:
        """
        Generate core models based on the provided schemas.

        This method iterates through the core schemas from the `schemas_manager`
        and generates models for each schema. For each core schema, it calls the
        `generate_model` method with the relevant parameters such as the schema type,
        base class, and model names.

        Args:
            schemas_manager (BuildSchemasManager): An instance of the schema manager
            containing the core schemas to be processed.

            model_names (DependencyModelNames): An instance containing the names of
            models used to handle dependencies between schemas.

        Returns:
            None
        """
    def generate_contrib_models(self, schemas_manager: BuildSchemasManager, model_names: DependencyModelNames) -> None:
        """
        Generate contributed models based on the provided schemas.

        This method processes the contributed schemas from the `schemas_manager`
        and generates models for each one. For each schema, it calls the
        `generate_model` method, passing the appropriate schema type, base class,
        model names, and the directory for contributed models.

        Args:
            schemas_manager (BuildSchemasManager): An instance of the schema manager
            containing the contributed schemas to be processed.

            model_names (DependencyModelNames): An instance containing the names of
            models used to handle dependencies between schemas.

        Returns:
            None
        """
    def generate_user_models(self, schemas_manager: BuildSchemasManager, model_names: DependencyModelNames) -> None:
        """
        Generate user-defined models based on the provided schemas.

        This method iterates through the user-defined schemas from the
        `schemas_manager` and generates models for each one. It invokes
        the `generate_model` method for every user schema, passing the
        relevant schema type, base class, model names, and the directory
        for user models.

        Args:
            schemas_manager (BuildSchemasManager): An instance of the schema manager
            that contains the user-defined schemas to be processed.

            model_names (DependencyModelNames): An instance containing the names of
            models used to handle dependencies between schemas.

        Returns:
            None
        """
    def generate_model(self, schema: ObjectSchema, schema_type: SchemaTypes, base_class: type[Model | TypeModel], model_names: DependencyModelNames, sub_models_directory: str) -> None:
        """
        Generate a model based on the provided schema and type.

        This method generates a model by processing a specific schema and
        its corresponding type (e.g., core, contrib, user). It also determines
        the appropriate base class and sub-model directory. The `model_names`
        argument is used to handle dependencies between schemas.

        Args:
            schema (ObjectSchema): The schema object to be processed for model generation.

            schema_type (SchemaTypes): The type of schema (e.g., TYPE, CORE, USER, CONTRIB)
            that defines the category of the model.

            base_class (type[Model | TypeModel]): The base class for the model being generated.

            model_names (DependencyModelNames): An instance containing model names used
            to resolve dependencies between schemas.

            sub_models_directory (str): The directory where sub-models corresponding
            to the schema will be placed.

        Returns:
            None
        """
    @staticmethod
    def _write_model(module_path: Path, class_source_builder: ClassSourceBuilder) -> None: ...
