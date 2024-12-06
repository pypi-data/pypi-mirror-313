import abc
import amsdal_glue as glue
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from amsdal_data.services.operation_manager import AsyncOperationManager, OperationManager
from amsdal_models.classes.model import Model as Model
from amsdal_models.querysets.base_queryset import QuerySetBase as QuerySetBase
from amsdal_models.querysets.errors import AmsdalQuerySetError as AmsdalQuerySetError
from amsdal_utils.models.data_models.address import Address
from amsdal_utils.query.enums import Lookup
from amsdal_utils.query.utils import Q
from typing import Any, Generic, TypeVar

logger: Incomplete
DEFAULT_DB_ALIAS: str
LAKEHOUSE_DB_ALIAS: str
OBJECT_ID_FIELD: str
OBJECT_VERSION_FIELD: str
CLASS_VERSION_FIELD: str
ADDRESS_FIELD: str
METADATA_FIELD: str
ModelType = TypeVar('ModelType', bound='Model')

class ExecutorBase(ABC, Generic[ModelType], metaclass=abc.ABCMeta):
    """
    Abstract base class for query executors.

    This class provides the base functionality for executing queries and counting
    results. It defines the interface that all concrete executor classes must implement.

    Attributes:
        queryset (QuerySetBase): The query set to be executed.
    """
    queryset: QuerySetBase[ModelType]
    def __init__(self, queryset: QuerySetBase[ModelType]) -> None: ...
    @property
    def operation_manager(self) -> OperationManager: ...
    @property
    def is_using_lakehouse(self) -> bool: ...
    @abstractmethod
    def query(self) -> list[dict[str, Any]]: ...
    @abstractmethod
    def count(self) -> int: ...

class AsyncExecutorBase(ABC, Generic[ModelType], metaclass=abc.ABCMeta):
    """
    Abstract base class for query executors.

    This class provides the base functionality for executing queries and counting
    results. It defines the interface that all concrete executor classes must implement.

    Attributes:
        queryset (QuerySetBase): The query set to be executed.
    """
    queryset: QuerySetBase[ModelType]
    def __init__(self, queryset: QuerySetBase[ModelType]) -> None: ...
    @property
    def operation_manager(self) -> AsyncOperationManager: ...
    @property
    def is_using_lakehouse(self) -> bool: ...
    @abstractmethod
    async def query(self) -> list[dict[str, Any]]: ...
    @abstractmethod
    async def count(self) -> int: ...

class Executor(ExecutorBase['ModelType']):
    """
    Concrete executor class for executing queries and counting results.

    This class extends the `ExecutorBase` and provides the implementation for
    executing queries and counting results using the specified query set.
    """
    def _address(self) -> Address: ...
    def query(self) -> list[dict[str, Any]]:
        """
        Execute the query and return the results.

        This method uses the connection object to execute the query based on the
        query set's specifier, conditions, pagination, and order by attributes.

        Returns:
            list[dict[str, Any]]: The query results as a list of dictionaries.
        """
    def count(self) -> int:
        """
        Execute the query and return the count of results.

        This method uses the connection object to execute the query and return
        the count of model instances that match the query conditions.

        Returns:
            int: The count of matching results.
        """
    def _process_select_related(self, select_related: dict[str, Any], model: type['ModelType'], alias_index: int = ...) -> dict[tuple[str, Address, str], Any]: ...
    def _process_data(self, data: dict[str, Any], select_related: dict[tuple[str, Address, str], Any] | None = ...) -> dict[str, Any]: ...
    def _build_query_statement(self, select_related: dict[tuple[str, Address, str], Any] | None = ..., *, is_count: bool = ...) -> glue.QueryStatement: ...
    def _build_joins(self, parent_alias: str, parent_properties: list[str], select_related: dict[tuple[str, Address, str], Any] | None) -> list[glue.JoinQuery] | None: ...
    def _build_only(self, select_related: dict[tuple[str, Address, str], Any] | None) -> list[glue.FieldReference] | None: ...
    def _build_joined_only(self, current_class_name: str, current_properties: list[str], select_related: dict[tuple[str, Address, str], Any]) -> list[glue.FieldReference]: ...
    def _build_nested_only(self, select_related: dict[tuple[str, Address, str], Any]) -> list[glue.FieldReferenceAliased]: ...
    def _resolve_nested_conditions(self, field_name: str, select_related: dict[tuple[str, Address, str], Any] | None = ...) -> tuple[str, str, tuple[str, Address, str] | None, dict[tuple[str, Address, str], Any] | None]: ...
    def _build_conditions(self, conditions: Q | None, select_related: dict[tuple[str, Address, str], Any] | None = ...) -> glue.Conditions | None: ...
    def _process_nested_rest(self, rest: str, select_related: dict[tuple[str, Address, str], Any] | None = ...) -> str: ...
    def _process_nested_lakehouse_rest(self, rest: str, select_related: dict[tuple[str, Address, str], Any] | None = ...) -> list[str]: ...
    @staticmethod
    def _build_field(field_name: str) -> glue.Field: ...
    def _build_order_by(self) -> list[glue.OrderByQuery] | None: ...
    def _build_limit(self) -> glue.LimitQuery | None: ...
    @staticmethod
    def _to_glue_lookup(lookup: Lookup) -> glue.FieldLookup: ...

class AsyncExecutor(AsyncExecutorBase['ModelType']):
    """
    Concrete executor class for executing queries and counting results.

    This class extends the `ExecutorBase` and provides the implementation for
    executing queries and counting results using the specified query set.
    """
    async def _address(self) -> Address: ...
    async def query(self) -> list[dict[str, Any]]:
        """
        Execute the query and return the results.

        This method uses the connection object to execute the query based on the
        query set's specifier, conditions, pagination, and order by attributes.

        Returns:
            list[dict[str, Any]]: The query results as a list of dictionaries.
        """
    async def count(self) -> int:
        """
        Execute the query and return the count of results.

        This method uses the connection object to execute the query and return
        the count of model instances that match the query conditions.

        Returns:
            int: The count of matching results.
        """
    def _process_select_related(self, select_related: dict[str, Any], model: type['ModelType'], alias_index: int = ...) -> dict[tuple[str, Address, str], Any]: ...
    async def _process_data(self, data: dict[str, Any], select_related: dict[tuple[str, Address, str], Any] | None = ...) -> dict[str, Any]: ...
    async def _build_query_statement(self, select_related: dict[tuple[str, Address, str], Any] | None = ..., *, is_count: bool = ...) -> glue.QueryStatement: ...
    async def _build_joins(self, parent_alias: str, parent_properties: list[str], select_related: dict[tuple[str, Address, str], Any] | None) -> list[glue.JoinQuery] | None: ...
    async def _build_only(self, select_related: dict[tuple[str, Address, str], Any] | None) -> list[glue.FieldReference] | None: ...
    async def _build_joined_only(self, current_class_name: str, current_properties: list[str], select_related: dict[tuple[str, Address, str], Any]) -> list[glue.FieldReference]: ...
    async def _build_nested_only(self, select_related: dict[tuple[str, Address, str], Any]) -> list[glue.FieldReferenceAliased]: ...
    def _resolve_nested_conditions(self, field_name: str, select_related: dict[tuple[str, Address, str], Any] | None = ...) -> tuple[str, str, tuple[str, Address, str] | None, dict[tuple[str, Address, str], Any] | None]: ...
    async def _build_conditions(self, conditions: Q | None, select_related: dict[tuple[str, Address, str], Any] | None = ...) -> glue.Conditions | None: ...
    def _process_nested_rest(self, rest: str, select_related: dict[tuple[str, Address, str], Any] | None = ...) -> str: ...
    async def _process_nested_lakehouse_rest(self, rest: str, select_related: dict[tuple[str, Address, str], Any] | None = ...) -> list[str]: ...
    @staticmethod
    def _build_field(field_name: str) -> glue.Field: ...
    def _build_order_by(self) -> list[glue.OrderByQuery] | None: ...
    def _build_limit(self) -> glue.LimitQuery | None: ...
    @staticmethod
    def _to_glue_lookup(lookup: Lookup) -> glue.FieldLookup: ...
