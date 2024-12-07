import logging
from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Any
from typing import Generic
from typing import TypeVar
from typing import Union

import amsdal_glue as glue
from amsdal_data.connections.constants import PRIMARY_PARTITION_KEY
from amsdal_data.connections.constants import SECONDARY_PARTITION_KEY
from amsdal_data.connections.historical.data_query_transform import METADATA_TABLE_ALIAS
from amsdal_data.connections.historical.data_query_transform import NEXT_VERSION_FIELD
from amsdal_data.connections.historical.schema_version_manager import AsyncHistoricalSchemaVersionManager
from amsdal_data.connections.historical.schema_version_manager import HistoricalSchemaVersionManager
from amsdal_data.services.operation_manager import AsyncOperationManager
from amsdal_data.services.operation_manager import OperationManager
from amsdal_utils.config.manager import AmsdalConfigManager
from amsdal_utils.errors import AmsdalError
from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.enums import SchemaTypes
from amsdal_utils.models.enums import Versions
from amsdal_utils.query.enums import Lookup
from amsdal_utils.query.enums import OrderDirection
from amsdal_utils.query.mixin import QueryableMixin
from amsdal_utils.query.utils import ConnectorEnum
from amsdal_utils.query.utils import Q

from amsdal_models.querysets.errors import AmsdalQuerySetError

if TYPE_CHECKING:
    from amsdal_models.classes.model import Model
    from amsdal_models.querysets.base_queryset import QuerySetBase

logger = logging.getLogger(__name__)

DEFAULT_DB_ALIAS = 'default'
LAKEHOUSE_DB_ALIAS = 'lakehouse'
OBJECT_ID_FIELD = 'object_id'
OBJECT_VERSION_FIELD = 'object_version'
CLASS_VERSION_FIELD = 'class_version'
ADDRESS_FIELD = '_address'
METADATA_FIELD = '_metadata'

ModelType = TypeVar('ModelType', bound='Model')


class ExecutorBase(Generic[ModelType], ABC):
    """
    Abstract base class for query executors.

    This class provides the base functionality for executing queries and counting
    results. It defines the interface that all concrete executor classes must implement.

    Attributes:
        queryset (QuerySetBase): The query set to be executed.
    """

    queryset: 'QuerySetBase[ModelType]'

    def __init__(self, queryset: 'QuerySetBase[ModelType]') -> None:
        self.queryset = queryset

    @property
    def operation_manager(self) -> OperationManager:
        from amsdal_data.application import DataApplication

        return DataApplication().operation_manager

    @property
    def is_using_lakehouse(self) -> bool:
        from amsdal_data.application import DataApplication

        return self.queryset.get_using() == LAKEHOUSE_DB_ALIAS or DataApplication().is_lakehouse_only

    @abstractmethod
    def query(self) -> list[dict[str, Any]]: ...

    @abstractmethod
    def count(self) -> int: ...


class AsyncExecutorBase(Generic[ModelType], ABC):
    """
    Abstract base class for query executors.

    This class provides the base functionality for executing queries and counting
    results. It defines the interface that all concrete executor classes must implement.

    Attributes:
        queryset (QuerySetBase): The query set to be executed.
    """

    queryset: 'QuerySetBase[ModelType]'

    def __init__(self, queryset: 'QuerySetBase[ModelType]') -> None:
        self.queryset = queryset

    @property
    def operation_manager(self) -> AsyncOperationManager:
        from amsdal_data.application import AsyncDataApplication

        return AsyncDataApplication().operation_manager

    @property
    def is_using_lakehouse(self) -> bool:
        from amsdal_data.application import AsyncDataApplication

        return self.queryset.get_using() == LAKEHOUSE_DB_ALIAS or AsyncDataApplication().is_lakehouse_only

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

    def _address(self) -> Address:
        return Address(
            resource='',
            class_name=self.queryset.entity_name,
            class_version=HistoricalSchemaVersionManager().get_latest_schema_version(self.queryset.entity_name),
            object_id='',
            object_version='',
        )

    def query(self) -> list[dict[str, Any]]:
        """
        Execute the query and return the results.

        This method uses the connection object to execute the query based on the
        query set's specifier, conditions, pagination, and order by attributes.

        Returns:
            list[dict[str, Any]]: The query results as a list of dictionaries.
        """
        if AmsdalConfigManager().get_config().async_mode:
            msg = 'Async mode is enabled. Use AsyncExecutor instead.'
            raise AmsdalError(msg)

        _select_related = None
        _unprocessed_select_related = self.queryset.get_select_related()
        if isinstance(_unprocessed_select_related, dict):
            _select_related = self._process_select_related(_unprocessed_select_related, self.queryset.entity)

        query = self._build_query_statement(select_related=_select_related)

        if self.is_using_lakehouse:
            result = self.operation_manager.query_lakehouse(query)
        else:
            result = self.operation_manager.query(query)

        if not result.success:
            msg = f'Error while executing query: {result.message}'
            raise AmsdalQuerySetError(msg) from result.exception

        return [self._process_data(item.data, _select_related) for item in (result.data or [])]

    def count(self) -> int:
        """
        Execute the query and return the count of results.

        This method uses the connection object to execute the query and return
        the count of model instances that match the query conditions.

        Returns:
            int: The count of matching results.
        """
        if AmsdalConfigManager().get_config().async_mode:
            msg = 'Async mode is enabled. Use AsyncExecutor instead.'
            raise AmsdalError(msg)

        query = self._build_query_statement(is_count=True)

        if self.is_using_lakehouse:
            result = self.operation_manager.query_lakehouse(query)
        else:
            result = self.operation_manager.query(query)

        if not result.success:
            msg = 'Error while executing query'
            raise Exception(msg) from result.exception

        return (result.data or [])[0].data['total_count']

    def _process_select_related(
        self,
        select_related: dict[str, Any],
        model: type['ModelType'],
        alias_index: int = 0,
    ) -> dict[tuple[str, Address, str], Any]:
        from amsdal_models.classes.model import LegacyModel
        from amsdal_models.classes.model import Model

        _select_related = {}

        for key, value in select_related.items():
            _field_type = model.model_fields[key].annotation

            if not _field_type or getattr(_field_type, '__origin__', None) != Union:
                msg = f'Select related field must be a Model type. Current field type: {_field_type}'
                raise ValueError(msg)

            base_class: type[ModelType] | None = next(
                (arg for arg in _field_type.__args__ if issubclass(arg, Model) and not issubclass(arg, LegacyModel)),
                None,
            )

            if not base_class:
                msg = f'Select related field must be a Model type. Current field type: {_field_type}'
                raise ValueError(msg)

            alias_index += 1
            _related = self._process_select_related(value, base_class, alias_index=alias_index)
            _select_related[
                (
                    key,
                    Address(
                        resource='',
                        class_name=base_class.__name__,
                        class_version=Versions.ALL,
                        object_id='',
                        object_version='',
                    ),
                    f'sr_{alias_index}',
                )
            ] = _related

        return _select_related

    def _process_data(
        self,
        data: dict[str, Any],
        select_related: dict[tuple[str, Address, str], Any] | None = None,
    ) -> dict[str, Any]:
        if select_related:
            for (field, address, alias), nested_select_related in select_related.items():
                nested_data = {}
                prefix = f'{alias}__'

                if self.is_using_lakehouse:
                    for version, _ in (
                        HistoricalSchemaVersionManager()
                        .get_all_schema_properties(
                            address.class_name,
                        )
                        .items()
                    ):
                        prefix += f'{version[:8]}__'

                        if any(True for field_name in data.keys() if field_name.startswith(prefix)):
                            break

                for data_field, value in data.items():
                    if data_field.startswith(prefix):
                        nested_data[data_field[slice(len(prefix), None)]] = value

                for key in nested_data.keys():
                    _prefixed_key = f'{prefix}{key}'

                    if _prefixed_key in data:
                        del data[_prefixed_key]

                nested_data = self._process_data(nested_data, nested_select_related)

                if nested_data and any(v is not None for v in nested_data.values()):
                    data[field] = nested_data

        if PRIMARY_PARTITION_KEY in data:
            data['_object_id'] = data.pop(PRIMARY_PARTITION_KEY)
        if SECONDARY_PARTITION_KEY in data:
            data.pop(SECONDARY_PARTITION_KEY)
        return data

    def _build_query_statement(
        self,
        select_related: dict[tuple[str, Address, str], Any] | None = None,
        *,
        is_count: bool = False,
    ) -> glue.QueryStatement:
        # TODO: add supporting of distinct into glue
        aggregation = None

        _only = self._build_only(select_related)
        if is_count:
            aggregation = glue.AggregationQuery(
                expression=glue.Count(
                    field=glue.FieldReference(
                        field=glue.Field(name='*'),
                        table_name=self.queryset.entity_name,
                    )
                ),
                alias='total_count',
            )
            _only = None

        _where = self._build_conditions(self.queryset.get_conditions(), select_related)

        return glue.QueryStatement(
            only=_only,
            aggregations=[aggregation] if aggregation else None,
            table=glue.SchemaReference(
                name=self.queryset.entity_name,
                version=HistoricalSchemaVersionManager().get_latest_schema_version(self.queryset.entity_name),
            ),
            joins=self._build_joins(
                self.queryset.entity_name,
                list(self.queryset.entity.model_fields.keys()),
                select_related,
            ),
            where=_where,
            order_by=self._build_order_by(),
            limit=self._build_limit(),
        )

    def _build_joins(
        self,
        parent_alias: str,
        parent_properties: list[str],
        select_related: dict[tuple[str, Address, str], Any] | None,
    ) -> list[glue.JoinQuery] | None:
        if not select_related:
            return None

        _joins = []

        for (field, address, alias), nested_select_related in select_related.items():
            if field not in parent_properties:
                logger.info(f'Field {field} not in parent "{parent_alias}" properties: {parent_properties}.')
                continue

            reference_field = glue.Field(name=field)
            ref_field = glue.Field(name='ref', parent=reference_field)
            object_id = glue.Field(name='object_id', parent=ref_field)
            reference_field.child = ref_field
            ref_field.child = object_id

            if self.is_using_lakehouse:
                for version, properties in (
                    HistoricalSchemaVersionManager()
                    .get_all_schema_properties(
                        address.class_name,
                    )
                    .items()
                ):
                    _alias = f'{alias}__{version[:8]}'

                    _property_names = list(properties.keys())
                    _property_names.extend([PRIMARY_PARTITION_KEY, SECONDARY_PARTITION_KEY])
                    q = glue.QueryStatement(
                        table=glue.SchemaReference(name=address.class_name, version=version),
                        only=self._build_joined_only(address.class_name, _property_names, nested_select_related),
                        joins=self._build_joins(address.class_name, _property_names, nested_select_related),
                    )

                    _joins.append(
                        glue.JoinQuery(
                            table=glue.SubQueryStatement(
                                query=q,
                                alias=_alias,
                            ),
                            on=glue.Conditions(
                                glue.Condition(
                                    field=glue.FieldReference(
                                        field=reference_field,
                                        table_name=parent_alias,
                                    ),
                                    lookup=glue.FieldLookup.EQ,
                                    value=glue.FieldReference(
                                        field=glue.Field(name=PRIMARY_PARTITION_KEY),
                                        table_name=_alias,
                                    ),
                                )
                            ),
                            join_type=glue.JoinType.LEFT,
                        )
                    )
            else:
                from amsdal_models.classes.manager import ClassManager

                reference_field = glue.Field(name=field)
                ref_field = glue.Field(name='ref', parent=reference_field)
                object_id = glue.Field(name='object_id', parent=ref_field)
                reference_field.child = ref_field
                ref_field.child = object_id

                model_class = ClassManager().import_model_class(address.class_name, SchemaTypes.USER)
                model_properties = list(model_class.model_fields.keys())
                model_properties.append(PRIMARY_PARTITION_KEY)
                q = glue.QueryStatement(
                    table=glue.SchemaReference(name=address.class_name, version=address.class_version),
                    only=self._build_joined_only(address.class_name, model_properties, nested_select_related),
                    joins=self._build_joins(address.class_name, model_properties, nested_select_related),
                )

                _joins.append(
                    glue.JoinQuery(
                        table=glue.SubQueryStatement(
                            query=q,
                            alias=alias,
                        ),
                        on=glue.Conditions(
                            glue.Condition(
                                field=glue.FieldReference(
                                    field=reference_field,
                                    table_name=parent_alias,
                                ),
                                lookup=glue.FieldLookup.EQ,
                                value=glue.FieldReference(
                                    field=glue.Field(name=PRIMARY_PARTITION_KEY),
                                    table_name=alias,
                                ),
                            )
                        ),
                        join_type=glue.JoinType.LEFT,
                    )
                )

        return _joins

    def _build_only(
        self,
        select_related: dict[tuple[str, Address, str], Any] | None,
    ) -> list[glue.FieldReference] | None:
        if self.queryset.get_query_specifier() and self.queryset.get_query_specifier().only:
            return [
                glue.FieldReference(
                    field=self._build_field(item),
                    table_name=self.queryset.entity_name,
                )
                for item in self.queryset.get_query_specifier().only
            ]

        if select_related:
            _only = []

            for prop_name in self.queryset.entity.model_fields:
                _only.append(
                    glue.FieldReference(
                        field=glue.Field(name=prop_name),
                        table_name=self.queryset.entity_name,
                    )
                )

            _only.extend(self._build_nested_only(select_related))

            return _only
        return None

    def _build_joined_only(
        self,
        current_class_name: str,
        current_properties: list[str],
        select_related: dict[tuple[str, Address, str], Any],
    ) -> list[glue.FieldReference]:
        _only = []

        for prop_name in current_properties:
            _only.append(
                glue.FieldReference(
                    field=glue.Field(name=prop_name),
                    table_name=current_class_name,
                )
            )

        if select_related:
            _only.extend(self._build_nested_only(select_related))

        return _only

    def _build_nested_only(
        self,
        select_related: dict[tuple[str, Address, str], Any],
    ) -> list[glue.FieldReferenceAliased]:
        _only: list[glue.FieldReferenceAliased] = []

        for (_, address, alias), nested_select_related in select_related.items():
            if self.is_using_lakehouse:
                for version, properties in (
                    HistoricalSchemaVersionManager()
                    .get_all_schema_properties(
                        address.class_name,
                    )
                    .items()
                ):
                    _alias = f'{alias}__{version[:8]}'
                    property_names = list(properties.keys())
                    property_names.extend([PRIMARY_PARTITION_KEY, SECONDARY_PARTITION_KEY])

                    for prop_name in property_names:
                        _only.append(
                            glue.FieldReferenceAliased(
                                field=glue.Field(name=prop_name),
                                table_name=_alias,
                                alias=f'{_alias}__{prop_name}',
                            )
                        )

                    if nested_select_related:
                        for sub_field in self._build_nested_only(nested_select_related):
                            _only.append(
                                glue.FieldReferenceAliased(
                                    field=glue.Field(name=sub_field.alias),
                                    table_name=_alias,
                                    alias=f'{_alias}__{sub_field.alias}',
                                )
                            )
            else:
                from amsdal_models.classes.manager import ClassManager

                model_class = ClassManager().import_model_class(address.class_name, SchemaTypes.USER)
                model_properties = list(model_class.model_fields.keys())
                model_properties.append(PRIMARY_PARTITION_KEY)

                for prop_name in model_properties:
                    _only.append(
                        glue.FieldReferenceAliased(
                            field=glue.Field(name=prop_name),
                            table_name=alias,
                            alias=f'{alias}__{prop_name}',
                        )
                    )

                if nested_select_related:
                    for sub_field in self._build_nested_only(nested_select_related):
                        _only.append(
                            glue.FieldReferenceAliased(
                                field=glue.Field(name=sub_field.alias),
                                table_name=alias,
                                alias=f'{alias}__{sub_field.alias}',
                            )
                        )

        return _only

    def _resolve_nested_conditions(
        self,
        field_name: str,
        select_related: dict[tuple[str, Address, str], Any] | None = None,
    ) -> tuple[str, str, tuple[str, Address, str] | None, dict[tuple[str, Address, str], Any] | None]:
        if '__' in field_name:
            [_field_name, _rest] = field_name.split('__', 1)
        else:
            [_field_name, _rest] = field_name, ''

        if select_related:
            _select_related_key: tuple[str, Address, str] | None = next(
                (key for key in select_related if key[0] == _field_name), None
            )
            _select_related = select_related.get(_select_related_key)  # type: ignore[arg-type]
            if _select_related:
                return self._resolve_nested_conditions(_rest, _select_related)
        else:
            _select_related_key = None
            _select_related = None

        return _field_name, _rest, _select_related_key, _select_related

    def _build_conditions(
        self,
        conditions: Q | None,
        select_related: dict[tuple[str, Address, str], Any] | None = None,
    ) -> glue.Conditions | None:
        if conditions:
            _conditions: list[glue.Conditions | glue.Condition] = []

            for child in conditions.children:
                if isinstance(child, Q):
                    if _cond := self._build_conditions(child, select_related):
                        _conditions.append(_cond)
                else:
                    if '__' in child.field_name:
                        [_field_name, _rest] = child.field_name.split('__', 1)
                    else:
                        [_field_name, _rest] = child.field_name, ''

                    if select_related:
                        _select_related_key: tuple[str, Address, str] | None = next(
                            (key for key in select_related if key[0] == _field_name), None
                        )
                        _select_related = select_related.get(_select_related_key)  # type: ignore[arg-type]
                    else:
                        _select_related_key = None
                        _select_related = None

                    _value = child.value

                    if isinstance(_value, QueryableMixin):
                        new_q = _value.to_query(prefix=f'{child.field_name}__')

                        if child.lookup == Lookup.NEQ:
                            new_q = ~new_q

                        if _cond := self._build_conditions(new_q, _select_related):
                            _conditions.append(_cond)
                        continue

                    if _field_name == ADDRESS_FIELD and not self.is_using_lakehouse and _rest != OBJECT_ID_FIELD:
                        # Ignore address field in non-lakehouse queries
                        continue

                    if _field_name == METADATA_FIELD and not self.is_using_lakehouse:
                        logger.warning(
                            'The "_metadata" field is not supported in non-lakehouse queries. It will be ignored.'
                        )
                        continue

                    if _field_name == ADDRESS_FIELD and _rest in (OBJECT_ID_FIELD, OBJECT_VERSION_FIELD):
                        if _rest == OBJECT_ID_FIELD:
                            _field = glue.Field(name=PRIMARY_PARTITION_KEY)
                        else:
                            _field = glue.Field(name=SECONDARY_PARTITION_KEY)

                            if _value in (glue.Version.LATEST, Versions.LATEST, '', 'LATEST'):
                                _conditions.append(
                                    glue.Conditions(
                                        glue.Condition(
                                            field=glue.FieldReference(
                                                field=glue.Field(name=NEXT_VERSION_FIELD),
                                                table_name=METADATA_TABLE_ALIAS,
                                            ),
                                            lookup=glue.FieldLookup.ISNULL,
                                            value=glue.Value(value=True),
                                        ),
                                        glue.Condition(
                                            field=glue.FieldReference(
                                                field=glue.Field(name=NEXT_VERSION_FIELD),
                                                table_name=METADATA_TABLE_ALIAS,
                                            ),
                                            lookup=glue.FieldLookup.EQ,
                                            value=glue.Value(value=''),
                                        ),
                                        connector=glue.FilterConnector.OR,
                                    ),
                                )
                                continue
                            elif _value in (glue.Version.ALL, Versions.ALL, 'ALL'):
                                _conditions.append(
                                    glue.Condition(
                                        field=glue.FieldReference(
                                            field=_field,
                                            table_name=self.queryset.entity_name,
                                        ),
                                        lookup=glue.FieldLookup.NEQ,
                                        value=glue.Value('_empty-'),
                                    )
                                )
                                continue
                    else:
                        _field = self._build_field(child.field_name)

                    if not _select_related_key:
                        _conditions.append(
                            glue.Condition(
                                field=glue.FieldReference(
                                    field=_field,
                                    table_name=self.queryset.entity_name,
                                ),
                                lookup=self._to_glue_lookup(child.lookup),
                                value=glue.Value(value=_value),
                            ),
                        )
                    elif self.is_using_lakehouse:
                        _rest_fields = self._process_nested_lakehouse_rest(_rest, _select_related)
                        versions = list(
                            HistoricalSchemaVersionManager()
                            .get_all_schema_properties(
                                _select_related_key[1].class_name,
                            )
                            .keys()
                        )
                        _conditions.append(
                            glue.Conditions(
                                *(
                                    glue.Condition(
                                        field=glue.FieldReference(
                                            field=glue.Field(name=f'{_rest}'),
                                            table_name=f'{_select_related_key[2]}__{version[:8]}',
                                        ),
                                        lookup=self._to_glue_lookup(child.lookup),
                                        value=glue.Value(value=_value),
                                    )
                                    for _rest in _rest_fields
                                    for version in versions
                                ),
                                connector=glue.FilterConnector.OR,
                            )
                        )
                    else:
                        _rest = self._process_nested_rest(_rest, _select_related)
                        _conditions.append(
                            glue.Conditions(
                                glue.Condition(
                                    field=glue.FieldReference(
                                        field=glue.Field(name=f'{_rest}'),
                                        table_name=_select_related_key[2],
                                    ),
                                    lookup=self._to_glue_lookup(child.lookup),
                                    value=glue.Value(value=_value),
                                ),
                                connector=glue.FilterConnector.OR,
                            ),
                        )

            return glue.Conditions(
                *_conditions,
                connector=(
                    {
                        ConnectorEnum.AND: glue.FilterConnector.AND,
                        ConnectorEnum.OR: glue.FilterConnector.OR,
                    }
                )[conditions.connector],
                negated=conditions.negated,
            )

        return None

    def _process_nested_rest(
        self,
        rest: str,
        select_related: dict[tuple[str, Address, str], Any] | None = None,
    ) -> str:
        if not select_related or '__' not in rest:
            return rest
        [_field_name, _rest] = rest.split('__', 1)

        for (field, _, alias), nested_select_related in select_related.items():
            if field == _field_name:
                return f'{alias}__{self._process_nested_rest(_rest, nested_select_related)}'
        return rest

    def _process_nested_lakehouse_rest(
        self,
        rest: str,
        select_related: dict[tuple[str, Address, str], Any] | None = None,
    ) -> list[str]:
        if not select_related or '__' not in rest:
            return [rest]
        [_field_name, _rest] = rest.split('__', 1)

        _fields = []
        for (field, address, alias), nested_select_related in select_related.items():
            if field == _field_name:
                versions = list(
                    HistoricalSchemaVersionManager()
                    .get_all_schema_properties(
                        address.class_name,
                    )
                    .keys()
                )
                _fields.extend(
                    [
                        f'{alias}__{version[:8]}__{sub_field}'
                        for version in versions
                        for sub_field in self._process_nested_lakehouse_rest(_rest, nested_select_related)
                    ]
                )
        return _fields

    @staticmethod
    def _build_field(field_name: str) -> glue.Field:
        if '__' in field_name:
            _parent_name, *_rest_names = field_name.split('__')
            field = glue.Field(name=_parent_name)
            _root = field

            for _name in _rest_names:
                _child = glue.Field(name=_name, parent=_root)
                _root.child = _child
                _root = _child
        else:
            field = glue.Field(name=field_name)
        return field

    def _build_order_by(self) -> list[glue.OrderByQuery] | None:
        if self.queryset.get_order_by():
            order = []

            for item in self.queryset.get_order_by():
                if '__' in item.field_name:
                    [_field_name, _rest] = item.field_name.split('__', 1)
                else:
                    [_field_name, _rest] = item.field_name, ''

                if _field_name == ADDRESS_FIELD and not self.is_using_lakehouse and _rest != OBJECT_ID_FIELD:
                    # Ignore address field in non-lakehouse queries
                    logger.warning(
                        'State database supports only ordering by _address__object_id field.  It will be ignored.',
                    )
                    continue

                if _field_name == METADATA_FIELD and not self.is_using_lakehouse:
                    logger.warning(
                        'The "_metadata" field is not supported in non-lakehouse queries. It will be ignored.',
                    )
                    continue

                order.append(
                    glue.OrderByQuery(
                        field=glue.FieldReference(
                            field=self._build_field(item.field_name),
                            table_name=self.queryset.entity_name,
                        ),
                        direction=(
                            {
                                OrderDirection.ASC: glue.OrderDirection.ASC,
                                OrderDirection.DESC: glue.OrderDirection.DESC,
                            }
                        )[item.direction],
                    ),
                )
            return order

        return None

    def _build_limit(self) -> glue.LimitQuery | None:
        if self.queryset.get_paginator():
            _limit = self.queryset.get_paginator().limit

            if _limit:
                return glue.LimitQuery(
                    limit=_limit,
                    offset=self.queryset.get_paginator().offset or 0,
                )

        return None

    @staticmethod
    def _to_glue_lookup(lookup: Lookup) -> glue.FieldLookup:
        return (
            {
                Lookup.EQ: glue.FieldLookup.EQ,
                Lookup.NEQ: glue.FieldLookup.NEQ,
                Lookup.GT: glue.FieldLookup.GT,
                Lookup.GTE: glue.FieldLookup.GTE,
                Lookup.LT: glue.FieldLookup.LT,
                Lookup.LTE: glue.FieldLookup.LTE,
                Lookup.IN: glue.FieldLookup.IN,
                Lookup.CONTAINS: glue.FieldLookup.CONTAINS,
                Lookup.ICONTAINS: glue.FieldLookup.ICONTAINS,
                Lookup.STARTSWITH: glue.FieldLookup.STARTSWITH,
                Lookup.ISTARTSWITH: glue.FieldLookup.ISTARTSWITH,
                Lookup.ENDSWITH: glue.FieldLookup.ENDSWITH,
                Lookup.IENDSWITH: glue.FieldLookup.IENDSWITH,
                Lookup.ISNULL: glue.FieldLookup.ISNULL,
                Lookup.REGEX: glue.FieldLookup.REGEX,
                Lookup.IREGEX: glue.FieldLookup.IREGEX,
            }
        )[lookup]


class AsyncExecutor(AsyncExecutorBase['ModelType']):
    """
    Concrete executor class for executing queries and counting results.

    This class extends the `ExecutorBase` and provides the implementation for
    executing queries and counting results using the specified query set.
    """

    async def _address(self) -> Address:
        return Address(
            resource='',
            class_name=self.queryset.entity_name,
            class_version=await AsyncHistoricalSchemaVersionManager().get_latest_schema_version(
                self.queryset.entity_name
            ),
            object_id='',
            object_version='',
        )

    async def query(self) -> list[dict[str, Any]]:
        """
        Execute the query and return the results.

        This method uses the connection object to execute the query based on the
        query set's specifier, conditions, pagination, and order by attributes.

        Returns:
            list[dict[str, Any]]: The query results as a list of dictionaries.
        """
        if not AmsdalConfigManager().get_config().async_mode:
            msg = 'Async mode is disabled. Use Executor instead.'
            raise AmsdalError(msg)

        _select_related = None
        _unprocessed_select_related = self.queryset.get_select_related()
        if isinstance(_unprocessed_select_related, dict):
            _select_related = self._process_select_related(_unprocessed_select_related, self.queryset.entity)

        query = await self._build_query_statement(select_related=_select_related)

        if self.is_using_lakehouse:
            result = await self.operation_manager.query_lakehouse(query)
        else:
            result = await self.operation_manager.query(query)

        if not result.success:
            msg = f'Error while executing query: {result.message}'
            raise AmsdalQuerySetError(msg) from result.exception

        return [await self._process_data(item.data, _select_related) for item in (result.data or [])]

    async def count(self) -> int:
        """
        Execute the query and return the count of results.

        This method uses the connection object to execute the query and return
        the count of model instances that match the query conditions.

        Returns:
            int: The count of matching results.
        """
        if not AmsdalConfigManager().get_config().async_mode:
            msg = 'Async mode is disabled. Use Executor instead.'
            raise AmsdalError(msg)

        query = await self._build_query_statement(is_count=True)

        if self.is_using_lakehouse:
            result = await self.operation_manager.query_lakehouse(query)
        else:
            result = await self.operation_manager.query(query)

        if not result.success:
            msg = 'Error while executing query'
            raise Exception(msg) from result.exception

        return (result.data or [])[0].data['total_count']

    def _process_select_related(
        self,
        select_related: dict[str, Any],
        model: type['ModelType'],
        alias_index: int = 0,
    ) -> dict[tuple[str, Address, str], Any]:
        from amsdal_models.classes.model import LegacyModel
        from amsdal_models.classes.model import Model

        _select_related = {}

        for key, value in select_related.items():
            _field_type = model.model_fields[key].annotation

            if not _field_type or getattr(_field_type, '__origin__', None) != Union:
                msg = f'Select related field must be a Model type. Current field type: {_field_type}'
                raise ValueError(msg)

            base_class: type[ModelType] | None = next(
                (arg for arg in _field_type.__args__ if issubclass(arg, Model) and not issubclass(arg, LegacyModel)),
                None,
            )

            if not base_class:
                msg = f'Select related field must be a Model type. Current field type: {_field_type}'
                raise ValueError(msg)

            alias_index += 1
            _related = self._process_select_related(value, base_class, alias_index=alias_index)
            _select_related[
                (
                    key,
                    Address(
                        resource='',
                        class_name=base_class.__name__,
                        class_version=Versions.ALL,
                        object_id='',
                        object_version='',
                    ),
                    f'sr_{alias_index}',
                )
            ] = _related

        return _select_related

    async def _process_data(
        self,
        data: dict[str, Any],
        select_related: dict[tuple[str, Address, str], Any] | None = None,
    ) -> dict[str, Any]:
        if select_related:
            for (field, address, alias), nested_select_related in select_related.items():
                nested_data = {}
                prefix = f'{alias}__'

                if self.is_using_lakehouse:
                    for version, _ in (
                        await AsyncHistoricalSchemaVersionManager().get_all_schema_properties(
                            address.class_name,
                        )
                    ).items():
                        prefix += f'{version[:8]}__'

                        if any(True for field_name in data.keys() if field_name.startswith(prefix)):
                            break

                for data_field, value in data.items():
                    if data_field.startswith(prefix):
                        nested_data[data_field[slice(len(prefix), None)]] = value

                for key in nested_data.keys():
                    _prefixed_key = f'{prefix}{key}'

                    if _prefixed_key in data:
                        del data[_prefixed_key]

                nested_data = await self._process_data(nested_data, nested_select_related)

                if nested_data and any(v is not None for v in nested_data.values()):
                    data[field] = nested_data

        if PRIMARY_PARTITION_KEY in data:
            data['_object_id'] = data.pop(PRIMARY_PARTITION_KEY)
        if SECONDARY_PARTITION_KEY in data:
            data['_object_version'] = data.pop(SECONDARY_PARTITION_KEY)
        return data

    async def _build_query_statement(
        self,
        select_related: dict[tuple[str, Address, str], Any] | None = None,
        *,
        is_count: bool = False,
    ) -> glue.QueryStatement:
        # TODO: add supporting of distinct into glue
        aggregation = None

        _only = await self._build_only(select_related)
        if is_count:
            aggregation = glue.AggregationQuery(
                expression=glue.Count(
                    field=glue.FieldReference(
                        field=glue.Field(name='*'),
                        table_name=self.queryset.entity_name,
                    )
                ),
                alias='total_count',
            )
            _only = None

        _where = await self._build_conditions(self.queryset.get_conditions(), select_related)

        return glue.QueryStatement(
            only=_only,
            aggregations=[aggregation] if aggregation else None,
            table=glue.SchemaReference(
                name=self.queryset.entity_name,
                version=await AsyncHistoricalSchemaVersionManager().get_latest_schema_version(
                    self.queryset.entity_name
                ),
            ),
            joins=await self._build_joins(
                self.queryset.entity_name,
                list(self.queryset.entity.model_fields.keys()),
                select_related,
            ),
            where=_where,
            order_by=self._build_order_by(),
            limit=self._build_limit(),
        )

    async def _build_joins(
        self,
        parent_alias: str,
        parent_properties: list[str],
        select_related: dict[tuple[str, Address, str], Any] | None,
    ) -> list[glue.JoinQuery] | None:
        if not select_related:
            return None

        _joins = []

        for (field, address, alias), nested_select_related in select_related.items():
            if field not in parent_properties:
                logger.info(f'Field {field} not in parent "{parent_alias}" properties: {parent_properties}.')
                continue

            reference_field = glue.Field(name=field)
            ref_field = glue.Field(name='ref', parent=reference_field)
            object_id = glue.Field(name='object_id', parent=ref_field)
            reference_field.child = ref_field
            ref_field.child = object_id

            if self.is_using_lakehouse:
                for version, properties in (
                    await AsyncHistoricalSchemaVersionManager().get_all_schema_properties(
                        address.class_name,
                    )
                ).items():
                    _alias = f'{alias}__{version[:8]}'

                    _property_names = list(properties.keys())
                    _property_names.extend([PRIMARY_PARTITION_KEY, SECONDARY_PARTITION_KEY])
                    q = glue.QueryStatement(
                        table=glue.SchemaReference(name=address.class_name, version=version),
                        only=await self._build_joined_only(address.class_name, _property_names, nested_select_related),
                        joins=await self._build_joins(address.class_name, _property_names, nested_select_related),
                    )

                    _joins.append(
                        glue.JoinQuery(
                            table=glue.SubQueryStatement(
                                query=q,
                                alias=_alias,
                            ),
                            on=glue.Conditions(
                                glue.Condition(
                                    field=glue.FieldReference(
                                        field=reference_field,
                                        table_name=parent_alias,
                                    ),
                                    lookup=glue.FieldLookup.EQ,
                                    value=glue.FieldReference(
                                        field=glue.Field(name=PRIMARY_PARTITION_KEY),
                                        table_name=_alias,
                                    ),
                                )
                            ),
                            join_type=glue.JoinType.LEFT,
                        )
                    )
            else:
                from amsdal_models.classes.manager import ClassManager

                reference_field = glue.Field(name=field)
                ref_field = glue.Field(name='ref', parent=reference_field)
                object_id = glue.Field(name='object_id', parent=ref_field)
                reference_field.child = ref_field
                ref_field.child = object_id

                model_class = ClassManager().import_model_class(address.class_name, SchemaTypes.USER)
                model_properties = list(model_class.model_fields.keys())
                model_properties.append(PRIMARY_PARTITION_KEY)
                q = glue.QueryStatement(
                    table=glue.SchemaReference(name=address.class_name, version=address.class_version),
                    only=await self._build_joined_only(address.class_name, model_properties, nested_select_related),
                    joins=await self._build_joins(address.class_name, model_properties, nested_select_related),
                )

                _joins.append(
                    glue.JoinQuery(
                        table=glue.SubQueryStatement(
                            query=q,
                            alias=alias,
                        ),
                        on=glue.Conditions(
                            glue.Condition(
                                field=glue.FieldReference(
                                    field=reference_field,
                                    table_name=parent_alias,
                                ),
                                lookup=glue.FieldLookup.EQ,
                                value=glue.FieldReference(
                                    field=glue.Field(name=PRIMARY_PARTITION_KEY),
                                    table_name=alias,
                                ),
                            )
                        ),
                        join_type=glue.JoinType.LEFT,
                    )
                )

        return _joins

    async def _build_only(
        self,
        select_related: dict[tuple[str, Address, str], Any] | None,
    ) -> list[glue.FieldReference] | None:
        if self.queryset.get_query_specifier() and self.queryset.get_query_specifier().only:
            return [
                glue.FieldReference(
                    field=self._build_field(item),
                    table_name=self.queryset.entity_name,
                )
                for item in self.queryset.get_query_specifier().only
            ]

        if select_related:
            _only = []

            for prop_name in self.queryset.entity.model_fields:
                _only.append(
                    glue.FieldReference(
                        field=glue.Field(name=prop_name),
                        table_name=self.queryset.entity_name,
                    )
                )

            _only.extend(await self._build_nested_only(select_related))

            return _only
        return None

    async def _build_joined_only(
        self,
        current_class_name: str,
        current_properties: list[str],
        select_related: dict[tuple[str, Address, str], Any],
    ) -> list[glue.FieldReference]:
        _only = []

        for prop_name in current_properties:
            _only.append(
                glue.FieldReference(
                    field=glue.Field(name=prop_name),
                    table_name=current_class_name,
                )
            )

        if select_related:
            _only.extend(await self._build_nested_only(select_related))

        return _only

    async def _build_nested_only(
        self,
        select_related: dict[tuple[str, Address, str], Any],
    ) -> list[glue.FieldReferenceAliased]:
        _only: list[glue.FieldReferenceAliased] = []

        for (_, address, alias), nested_select_related in select_related.items():
            if self.is_using_lakehouse:
                for version, properties in (
                    await AsyncHistoricalSchemaVersionManager().get_all_schema_properties(
                        address.class_name,
                    )
                ).items():
                    _alias = f'{alias}__{version[:8]}'
                    property_names = list(properties.keys())
                    property_names.extend([PRIMARY_PARTITION_KEY, SECONDARY_PARTITION_KEY])

                    for prop_name in property_names:
                        _only.append(
                            glue.FieldReferenceAliased(
                                field=glue.Field(name=prop_name),
                                table_name=_alias,
                                alias=f'{_alias}__{prop_name}',
                            )
                        )

                    if nested_select_related:
                        for sub_field in await self._build_nested_only(nested_select_related):
                            _only.append(
                                glue.FieldReferenceAliased(
                                    field=glue.Field(name=sub_field.alias),
                                    table_name=_alias,
                                    alias=f'{_alias}__{sub_field.alias}',
                                )
                            )
            else:
                from amsdal_models.classes.manager import ClassManager

                model_class = ClassManager().import_model_class(address.class_name, SchemaTypes.USER)
                model_properties = list(model_class.model_fields.keys())
                model_properties.append(PRIMARY_PARTITION_KEY)

                for prop_name in model_properties:
                    _only.append(
                        glue.FieldReferenceAliased(
                            field=glue.Field(name=prop_name),
                            table_name=alias,
                            alias=f'{alias}__{prop_name}',
                        )
                    )

                if nested_select_related:
                    for sub_field in await self._build_nested_only(nested_select_related):
                        _only.append(
                            glue.FieldReferenceAliased(
                                field=glue.Field(name=sub_field.alias),
                                table_name=alias,
                                alias=f'{alias}__{sub_field.alias}',
                            )
                        )

        return _only

    def _resolve_nested_conditions(
        self,
        field_name: str,
        select_related: dict[tuple[str, Address, str], Any] | None = None,
    ) -> tuple[str, str, tuple[str, Address, str] | None, dict[tuple[str, Address, str], Any] | None]:
        if '__' in field_name:
            [_field_name, _rest] = field_name.split('__', 1)
        else:
            [_field_name, _rest] = field_name, ''

        if select_related:
            _select_related_key: tuple[str, Address, str] | None = next(
                (key for key in select_related if key[0] == _field_name), None
            )
            _select_related = select_related.get(_select_related_key)  # type: ignore[arg-type]
            if _select_related:
                return self._resolve_nested_conditions(_rest, _select_related)
        else:
            _select_related_key = None
            _select_related = None

        return _field_name, _rest, _select_related_key, _select_related

    async def _build_conditions(
        self,
        conditions: Q | None,
        select_related: dict[tuple[str, Address, str], Any] | None = None,
    ) -> glue.Conditions | None:
        if conditions:
            _conditions: list[glue.Conditions | glue.Condition] = []

            for child in conditions.children:
                if isinstance(child, Q):
                    if _cond := await self._build_conditions(child, select_related):
                        _conditions.append(_cond)
                else:
                    if '__' in child.field_name:
                        [_field_name, _rest] = child.field_name.split('__', 1)
                    else:
                        [_field_name, _rest] = child.field_name, ''

                    if select_related:
                        _select_related_key: tuple[str, Address, str] | None = next(
                            (key for key in select_related if key[0] == _field_name), None
                        )
                        _select_related = select_related.get(_select_related_key)  # type: ignore[arg-type]
                    else:
                        _select_related_key = None
                        _select_related = None

                    _value = child.value

                    if isinstance(_value, QueryableMixin):
                        new_q = _value.to_query(prefix=f'{child.field_name}__')

                        if child.lookup == Lookup.NEQ:
                            new_q = ~new_q

                        if _cond := await self._build_conditions(new_q, _select_related):
                            _conditions.append(_cond)
                        continue

                    if _field_name == ADDRESS_FIELD and not self.is_using_lakehouse and _rest != OBJECT_ID_FIELD:
                        # Ignore address field in non-lakehouse queries
                        continue

                    if _field_name == METADATA_FIELD and not self.is_using_lakehouse:
                        logger.warning(
                            'The "_metadata" field is not supported in non-lakehouse queries. It will be ignored.'
                        )
                        continue

                    if _field_name == ADDRESS_FIELD and _rest in (OBJECT_ID_FIELD, OBJECT_VERSION_FIELD):
                        if _rest == OBJECT_ID_FIELD:
                            _field = glue.Field(name=PRIMARY_PARTITION_KEY)
                        else:
                            _field = glue.Field(name=SECONDARY_PARTITION_KEY)

                            if _value in (glue.Version.LATEST, Versions.LATEST, '', 'LATEST'):
                                _conditions.append(
                                    glue.Conditions(
                                        glue.Condition(
                                            field=glue.FieldReference(
                                                field=glue.Field(name=NEXT_VERSION_FIELD),
                                                table_name=METADATA_TABLE_ALIAS,
                                            ),
                                            lookup=glue.FieldLookup.ISNULL,
                                            value=glue.Value(value=True),
                                        ),
                                        glue.Condition(
                                            field=glue.FieldReference(
                                                field=glue.Field(name=NEXT_VERSION_FIELD),
                                                table_name=METADATA_TABLE_ALIAS,
                                            ),
                                            lookup=glue.FieldLookup.EQ,
                                            value=glue.Value(value=''),
                                        ),
                                        connector=glue.FilterConnector.OR,
                                    ),
                                )
                                continue
                            elif _value in (glue.Version.ALL, Versions.ALL, 'ALL'):
                                _conditions.append(
                                    glue.Condition(
                                        field=glue.FieldReference(
                                            field=_field,
                                            table_name=self.queryset.entity_name,
                                        ),
                                        lookup=glue.FieldLookup.NEQ,
                                        value=glue.Value('_empty-'),
                                    )
                                )
                                continue
                    else:
                        _field = self._build_field(child.field_name)

                    if not _select_related_key:
                        _conditions.append(
                            glue.Condition(
                                field=glue.FieldReference(
                                    field=_field,
                                    table_name=self.queryset.entity_name,
                                ),
                                lookup=self._to_glue_lookup(child.lookup),
                                value=glue.Value(value=_value),
                            ),
                        )
                    elif self.is_using_lakehouse:
                        _rest_fields = await self._process_nested_lakehouse_rest(_rest, _select_related)
                        versions = list(
                            (
                                await AsyncHistoricalSchemaVersionManager().get_all_schema_properties(
                                    _select_related_key[1].class_name,
                                )
                            ).keys()
                        )
                        _conditions.append(
                            glue.Conditions(
                                *(
                                    glue.Condition(
                                        field=glue.FieldReference(
                                            field=glue.Field(name=f'{_rest}'),
                                            table_name=f'{_select_related_key[2]}__{version[:8]}',
                                        ),
                                        lookup=self._to_glue_lookup(child.lookup),
                                        value=glue.Value(value=_value),
                                    )
                                    for _rest in _rest_fields
                                    for version in versions
                                ),
                                connector=glue.FilterConnector.OR,
                            )
                        )
                    else:
                        _rest = self._process_nested_rest(_rest, _select_related)
                        _conditions.append(
                            glue.Conditions(
                                glue.Condition(
                                    field=glue.FieldReference(
                                        field=glue.Field(name=f'{_rest}'),
                                        table_name=_select_related_key[2],
                                    ),
                                    lookup=self._to_glue_lookup(child.lookup),
                                    value=glue.Value(value=_value),
                                ),
                                connector=glue.FilterConnector.OR,
                            ),
                        )

            return glue.Conditions(
                *_conditions,
                connector=(
                    {
                        ConnectorEnum.AND: glue.FilterConnector.AND,
                        ConnectorEnum.OR: glue.FilterConnector.OR,
                    }
                )[conditions.connector],
                negated=conditions.negated,
            )

        return None

    def _process_nested_rest(
        self,
        rest: str,
        select_related: dict[tuple[str, Address, str], Any] | None = None,
    ) -> str:
        if not select_related or '__' not in rest:
            return rest
        [_field_name, _rest] = rest.split('__', 1)

        for (field, _, alias), nested_select_related in select_related.items():
            if field == _field_name:
                return f'{alias}__{self._process_nested_rest(_rest, nested_select_related)}'
        return rest

    async def _process_nested_lakehouse_rest(
        self,
        rest: str,
        select_related: dict[tuple[str, Address, str], Any] | None = None,
    ) -> list[str]:
        if not select_related or '__' not in rest:
            return [rest]
        [_field_name, _rest] = rest.split('__', 1)

        _fields = []
        for (field, address, alias), nested_select_related in select_related.items():
            if field == _field_name:
                versions = list(
                    (
                        await AsyncHistoricalSchemaVersionManager().get_all_schema_properties(
                            address.class_name,
                        )
                    ).keys()
                )
                _fields.extend(
                    [
                        f'{alias}__{version[:8]}__{sub_field}'
                        for version in versions
                        for sub_field in await self._process_nested_lakehouse_rest(_rest, nested_select_related)
                    ]
                )
        return _fields

    @staticmethod
    def _build_field(field_name: str) -> glue.Field:
        if '__' in field_name:
            _parent_name, *_rest_names = field_name.split('__')
            field = glue.Field(name=_parent_name)
            _root = field

            for _name in _rest_names:
                _child = glue.Field(name=_name, parent=_root)
                _root.child = _child
                _root = _child
        else:
            field = glue.Field(name=field_name)
        return field

    def _build_order_by(self) -> list[glue.OrderByQuery] | None:
        if self.queryset.get_order_by():
            order = []

            for item in self.queryset.get_order_by():
                if '__' in item.field_name:
                    [_field_name, _rest] = item.field_name.split('__', 1)
                else:
                    [_field_name, _rest] = item.field_name, ''

                if _field_name == ADDRESS_FIELD and not self.is_using_lakehouse and _rest != OBJECT_ID_FIELD:
                    # Ignore address field in non-lakehouse queries
                    logger.warning(
                        'State database supports only ordering by _address__object_id field.  It will be ignored.',
                    )
                    continue

                if _field_name == METADATA_FIELD and not self.is_using_lakehouse:
                    logger.warning(
                        'The "_metadata" field is not supported in non-lakehouse queries. It will be ignored.',
                    )
                    continue

                order.append(
                    glue.OrderByQuery(
                        field=glue.FieldReference(
                            field=self._build_field(item.field_name),
                            table_name=self.queryset.entity_name,
                        ),
                        direction=(
                            {
                                OrderDirection.ASC: glue.OrderDirection.ASC,
                                OrderDirection.DESC: glue.OrderDirection.DESC,
                            }
                        )[item.direction],
                    ),
                )
            return order

        return None

    def _build_limit(self) -> glue.LimitQuery | None:
        if self.queryset.get_paginator():
            _limit = self.queryset.get_paginator().limit

            if _limit:
                return glue.LimitQuery(
                    limit=_limit,
                    offset=self.queryset.get_paginator().offset or 0,
                )

        return None

    @staticmethod
    def _to_glue_lookup(lookup: Lookup) -> glue.FieldLookup:
        return (
            {
                Lookup.EQ: glue.FieldLookup.EQ,
                Lookup.NEQ: glue.FieldLookup.NEQ,
                Lookup.GT: glue.FieldLookup.GT,
                Lookup.GTE: glue.FieldLookup.GTE,
                Lookup.LT: glue.FieldLookup.LT,
                Lookup.LTE: glue.FieldLookup.LTE,
                Lookup.IN: glue.FieldLookup.IN,
                Lookup.CONTAINS: glue.FieldLookup.CONTAINS,
                Lookup.ICONTAINS: glue.FieldLookup.ICONTAINS,
                Lookup.STARTSWITH: glue.FieldLookup.STARTSWITH,
                Lookup.ISTARTSWITH: glue.FieldLookup.ISTARTSWITH,
                Lookup.ENDSWITH: glue.FieldLookup.ENDSWITH,
                Lookup.IENDSWITH: glue.FieldLookup.IENDSWITH,
                Lookup.ISNULL: glue.FieldLookup.ISNULL,
                Lookup.REGEX: glue.FieldLookup.REGEX,
                Lookup.IREGEX: glue.FieldLookup.IREGEX,
            }
        )[lookup]
