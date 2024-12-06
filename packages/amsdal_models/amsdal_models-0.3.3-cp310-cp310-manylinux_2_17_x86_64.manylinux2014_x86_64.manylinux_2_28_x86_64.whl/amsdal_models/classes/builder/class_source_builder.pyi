from _typeshed import Incomplete
from amsdal_models.classes.builder.ast_generator.class_generator import AstClassGenerator as AstClassGenerator
from amsdal_models.classes.data_models.dependencies import DependencyModelNames as DependencyModelNames
from amsdal_models.classes.model import Model as Model, TypeModel as TypeModel
from amsdal_models.schemas.utils.schema_fingerprint import calculate_schema_fingerprint as calculate_schema_fingerprint
from amsdal_utils.models.data_models.schema import ObjectSchema as ObjectSchema
from amsdal_utils.models.enums import SchemaTypes as SchemaTypes
from functools import cached_property as cached_property

class ClassSourceBuilder:
    ast_generator: AstClassGenerator
    _schema: Incomplete
    _schema_type: Incomplete
    _base_class: Incomplete
    def __init__(self, models_module_name: str, schema: ObjectSchema, schema_type: SchemaTypes, base_class: type[Model | TypeModel], model_names: DependencyModelNames) -> None:
        """
        Initializes the ClassSourceBuilder.

        Args:
            models_module_name (str): The name of the models module.
            schema (ObjectSchema): The schema object.
            schema_type (SchemaTypes): The type of the schema.
            base_class (type[Model | TypeModel]): The base class for the model.
            model_names (DependencyModelNames): The model names for dependencies.

        Returns:
            None
        """
    @cached_property
    def model_class_source(self) -> str:
        """
        Returns the source code for the model class.

        Returns:
            str: The source code for the model class.
        """
    @cached_property
    def dependencies_source(self) -> str:
        """
        Returns the source code for the dependencies.

        Returns:
            str: The source code for the dependencies.
        """
    def _build_class_source(self) -> str: ...
