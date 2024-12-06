import ast
from amsdal_models.classes.builder.ast_generator.dependency_generator import AstDependencyGenerator as AstDependencyGenerator
from amsdal_models.classes.constants import BASIC_TYPES_MAP as BASIC_TYPES_MAP
from amsdal_models.classes.model import LegacyModel as LegacyModel
from amsdal_utils.models.data_models.core import TypeData

def build_annotation_node(type_data: TypeData, *, is_required: bool = ..., can_be_a_reference: bool = ..., ast_dependency_generator: AstDependencyGenerator) -> ast.Subscript | ast.Constant | ast.Name | ast.BinOp:
    """
    Builds an AST node for type annotations.

    Args:
        type_data (TypeData): The type data for the annotation.
        is_required (bool, optional): Whether the type is required. Defaults to True.
        can_be_a_reference (bool, optional): Whether the type can be a reference. Defaults to True.
        ast_dependency_generator (AstDependencyGenerator): The AST dependency generator.

    Returns:
        ast.Subscript | ast.Constant | ast.Name | ast.BinOp: The AST node representing the type annotation.
    """
