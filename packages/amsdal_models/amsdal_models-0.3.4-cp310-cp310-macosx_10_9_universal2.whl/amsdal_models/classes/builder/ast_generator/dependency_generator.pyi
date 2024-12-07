import ast
from _typeshed import Incomplete
from amsdal_models.classes.constants import CONTRIB_MODELS_MODULE as CONTRIB_MODELS_MODULE, CORE_MODELS_MODULE as CORE_MODELS_MODULE, USER_MODELS_MODULE as USER_MODELS_MODULE
from amsdal_models.classes.data_models.dependencies import DependencyItem as DependencyItem, DependencyModelNames as DependencyModelNames
from typing import Any

class AstDependencyGenerator:
    _ignore_type_names: Incomplete
    _models_module_name: Incomplete
    _model_names: Incomplete
    _dependencies: Incomplete
    def __init__(self, models_module_name: str, model_names: DependencyModelNames) -> None: ...
    @property
    def ast_module(self) -> ast.Module:
        """
        Generates an AST module for the dependencies.

        Returns:
            ast.Module: The AST module containing the import statements for the dependencies.
        """
    def add_ignore_type_name(self, type_name: str) -> None:
        """
        Ignores some type names and does not add them to the dependencies,
        probably in the case of self-referencing types.

        Args:
            type_name (str): The type name to ignore.

        Returns:
            None
        """
    def add_python_type_dependency(self, python_type: Any) -> None:
        """
        Adds a dependency for a given Python type.

        Args:
            python_type (Any): The Python type to add as a dependency.

        Returns:
            None
        """
    def add_model_type_dependency(self, model_type: str) -> None:
        """
        Adds a dependency for a given model type.

        Args:
            model_type (str): The model type to add as a dependency.

        Returns:
            None
        """
    def add_ast_import_node(self, node: ast.Import | ast.ImportFrom) -> None:
        """
        Adds an AST import node to the dependencies.

        Args:
            node (ast.Import | ast.ImportFrom): The AST import node to add.

        Returns:
            None
        """
