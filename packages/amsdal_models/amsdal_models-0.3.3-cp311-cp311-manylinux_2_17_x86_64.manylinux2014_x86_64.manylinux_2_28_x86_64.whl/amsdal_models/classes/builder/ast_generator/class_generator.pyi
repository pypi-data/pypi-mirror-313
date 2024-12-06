import ast
from _typeshed import Incomplete
from amsdal_models.classes.builder.ast_generator.data_models import CustomCodeAst as CustomCodeAst, NestedPropertyTypeAst as NestedPropertyTypeAst, PropertyAst as PropertyAst, PropertyValueAst as PropertyValueAst
from amsdal_models.classes.builder.ast_generator.dependency_generator import AstDependencyGenerator as AstDependencyGenerator
from amsdal_models.classes.builder.ast_generator.helpers.build_assign_node import build_assign_node as build_assign_node
from amsdal_models.classes.builder.ast_generator.helpers.build_validator_node import build_validator_node as build_validator_node
from amsdal_models.classes.builder.validator_resolver import ValidatorResolver as ValidatorResolver
from amsdal_models.classes.constants import BASE_OBJECT_TYPE as BASE_OBJECT_TYPE
from amsdal_models.classes.data_models.dependencies import DependencyModelNames as DependencyModelNames
from amsdal_models.classes.model import Model as Model, TypeModel as TypeModel
from amsdal_utils.models.data_models.schema import PropertyData as PropertyData
from amsdal_utils.models.enums import SchemaTypes

class AstClassGenerator:
    _base_class: Incomplete
    _class_definition: Incomplete
    _ast_dependency_generator: Incomplete
    def __init__(self, models_module_name: str, base_class: type[Model | TypeModel], model_names: DependencyModelNames) -> None: ...
    def register_class(self, class_name: str, extend_type: str) -> None:
        """
        Registers a class with the given name and extend type.

        Args:
            class_name (str): The name of the class to register.
            extend_type (str): The type to extend for the class.

        Returns:
            None
        """
    def add_class_data(self, schema_type: SchemaTypes, class_fingerprint: str) -> None:
        """
        Adds class data to the AST class definition.

        Args:
            schema_type (SchemaTypes): The schema type of the class.
            class_fingerprint (str): The fingerprint of the class.
        """
    def add_class_property(self, property_name: str, property_config: PropertyData, *, is_required: bool) -> None:
        """
        Adds a property to the AST class definition.

        Args:
            property_name (str): The name of the property to add.
            property_config (PropertyData): The configuration of the property.
            is_required (bool): Whether the property is required.

        Returns:
            None
        """
    def add_properties_validators(self, property_name: str, property_config: PropertyData) -> None:
        """
        Adds validators for the given property to the AST class definition.

        Args:
            property_name (str): The name of the property to validate.
            property_config (PropertyData): The configuration of the property.

        Returns:
            None
        """
    def add_class_custom_code(self, custom_code: str) -> None:
        """
        Adds custom code to the AST class definition.

        Args:
            custom_code (str): The custom code to add.

        Returns:
            None
        """
    @property
    def model_source(self) -> str:
        """
        Generates the source code for the model.

        Returns:
            str: The formatted source code of the model.
        """
    @property
    def dependencies_source(self) -> str:
        """
        Generates the source code for the dependencies.

        Returns:
            str: The formatted source code of the dependencies.
        """
    def _set_union_mode(self, node: ast.AnnAssign | ast.stmt) -> None: ...
