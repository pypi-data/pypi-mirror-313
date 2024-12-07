import logging
from typing import Any
from typing import Generic

import amsdal_glue as glue
from amsdal_data.connections.constants import PRIMARY_PARTITION_KEY
from amsdal_data.connections.constants import SECONDARY_PARTITION_KEY
from amsdal_data.connections.historical.data_query_transform import METADATA_TABLE_ALIAS
from amsdal_data.connections.historical.data_query_transform import NEXT_VERSION_FIELD
from amsdal_data.connections.historical.schema_version_manager import AsyncHistoricalSchemaVersionManager
from amsdal_data.connections.historical.schema_version_manager import HistoricalSchemaVersionManager
from amsdal_data.transactions.decorators import async_transaction
from amsdal_data.transactions.decorators import transaction
from amsdal_data.transactions.manager import AmsdalAsyncTransactionManager
from amsdal_data.transactions.manager import AmsdalTransactionManager
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_utils.models.enums import Versions
from amsdal_utils.query.utils import Q

from amsdal_models.classes.glue_utils import model_to_data
from amsdal_models.querysets.base_queryset import ModelType
from amsdal_models.querysets.base_queryset import QuerySet
from amsdal_models.querysets.base_queryset import QuerySetOne
from amsdal_models.querysets.base_queryset import QuerySetOneRequired
from amsdal_models.querysets.errors import BulkOperationError
from amsdal_models.querysets.executor import LAKEHOUSE_DB_ALIAS

logger = logging.getLogger(__name__)


class BaseManager(Generic[ModelType]):
    """
    Base manager for creating QuerySets for models.

    This class provides a base for managing models and creating query sets.
    It is generic and works with different model types defined by `ModelType`.

    Attributes:
        model (type[ModelType]): The model class associated with this manager.
        It defines the type of model this manager will handle.
    """

    model: type[ModelType]

    @property
    def _transaction_manager(self) -> AmsdalTransactionManager:
        return AmsdalTransactionManager()

    def copy(self, cls: type[ModelType]) -> 'BaseManager[ModelType]':
        """
        Create a copy of the current manager for a specified model class.

        This method creates a new instance of the manager, assigning the provided
        model class to the `model` attribute of the new instance. It returns a
        new `BaseManager` instance associated with the given model class.

        Args:
            cls (type[ModelType]): The model class for which the new manager
            instance will be created.

        Returns:
            BaseManager: A new instance of `BaseManager` associated with the
            specified model class.
        """
        manager = self.__class__()
        manager.model = cls

        return manager

    def get_queryset(self) -> QuerySet[ModelType]:
        """
        Retrieve a new QuerySet instance for the associated model.

        This method creates and returns a new `QuerySet` instance that is
        associated with the model class defined in the `model` attribute
        of the manager.

        Returns:
            QuerySet[ModelType]: A new `QuerySet` instance for the associated model.
        """
        return QuerySet(self.model)

    def using(self, value: str) -> QuerySet[ModelType]:
        """
        Set the database alias for the QuerySet.

        This method sets the database alias to be used for the QuerySet operations.
        It returns a new QuerySet instance that will use the specified database alias.

        Args:
            value (str): The database alias to be used for the QuerySet.

        Returns:
            QuerySet[ModelType]: A new QuerySet instance using the specified database alias.
        """
        return self.get_queryset().using(value)

    def all(self) -> QuerySet[ModelType]:
        """
        Retrieve all instances of the associated model.

        This method returns a new `QuerySet` instance that includes all
        instances of the model class defined in the `model` attribute
        of the manager.

        Returns:
            QuerySet[ModelType]: A new `QuerySet` instance containing all instances of the associated model.
        """
        return self.get_queryset()

    def only(self, fields: list[str]) -> QuerySet[ModelType]:
        """
        Retrieve a QuerySet with only the specified fields.

        This method returns a new `QuerySet` instance that includes only the
        specified fields of the model class defined in the `model` attribute
        of the manager.

        Args:
            fields (list[str]): A list of field names to include in the QuerySet.

        Returns:
            QuerySet[ModelType]: A new `QuerySet` instance containing only the specified fields.
        """
        return self.get_queryset().only(fields=fields)

    def distinct(self, fields: list[str]) -> QuerySet[ModelType]:
        """
        Retrieve a QuerySet with distinct values for the specified fields.

        This method returns a new `QuerySet` instance that includes only distinct
        values for the specified fields of the model class defined in the `model`
        attribute of the manager.

        Args:
            fields (list[str]): A list of field names for which to retrieve distinct values.

        Returns:
            QuerySet[ModelType]: A new `QuerySet` instance containing distinct values for the specified fields.
        """
        return self.get_queryset().distinct(fields=fields)

    def filter(self, *args: Q, **kwargs: Any) -> QuerySet[ModelType]:
        """
        Filter the QuerySet based on the given conditions.

        This method returns a new `QuerySet` instance that includes only the
        instances of the model class defined in the `model` attribute of the
        manager that match the specified conditions.

        Args:
            *args (Q): Positional arguments representing query conditions.
            **kwargs (Any): Keyword arguments representing query conditions.

        Returns:
            QuerySet[ModelType]: A new `QuerySet` instance containing the filtered results.
        """
        return self.get_queryset().filter(*args, **kwargs)

    def exclude(self, *args: Q, **kwargs: Any) -> QuerySet[ModelType]:
        """
        Exclude instances from the QuerySet based on the given conditions.

        This method returns a new `QuerySet` instance that excludes the
        instances of the model class defined in the `model` attribute of the
        manager that match the specified conditions.

        Args:
            *args (Q): Positional arguments representing query conditions.
            **kwargs (Any): Keyword arguments representing query conditions.

        Returns:
            QuerySet[ModelType]: A new `QuerySet` instance excluding the specified results.
        """
        return self.get_queryset().exclude(*args, **kwargs)

    def get(self, *args: Q, **kwargs: Any) -> QuerySetOneRequired[ModelType]:
        """
        Retrieve a single instance of the model that matches the given conditions.

        This method returns a `QuerySetOneRequired` instance that includes the
        instance of the model class defined in the `model` attribute of the manager
        that matches the specified conditions. If no instance matches the conditions,
        an exception is raised.

        Args:
            *args (Q): Positional arguments representing query conditions.
            **kwargs (Any): Keyword arguments representing query conditions.

        Returns:
            QuerySetOneRequired[ModelType]: A `QuerySetOneRequired` instance containing the matched instance.
        """
        return self.get_queryset().get(*args, **kwargs)

    def get_or_none(self, *args: Q, **kwargs: Any) -> QuerySetOne[ModelType]:
        """
        Retrieve a single instance of the model that matches the given conditions or None.

        This method returns a `QuerySetOne` instance that includes the instance of the
        model class defined in the `model` attribute of the manager that matches the
        specified conditions. If no instance matches the conditions, None is returned.

        Args:
            *args (Q): Positional arguments representing query conditions.
            **kwargs (Any): Keyword arguments representing query conditions.

        Returns:
            QuerySetOne[ModelType]: A `QuerySetOne` instance containing the matched instance or None.
        """
        return self.get_queryset().get_or_none(*args, **kwargs)

    def first(self, *args: Q, **kwargs: Any) -> QuerySetOne[ModelType]:
        """
        Retrieve the first instance of the model that matches the given conditions.

        This method returns a `QuerySetOne` instance that includes the first instance
        of the model class defined in the `model` attribute of the manager that matches
        the specified conditions. If no instance matches the conditions, None is returned.

        Args:
            *args (Q): Positional arguments representing query conditions.
            **kwargs (Any): Keyword arguments representing query conditions.

        Returns:
            QuerySetOne[ModelType]: A `QuerySetOne` instance containing the first matched instance or None.
        """
        return self.get_queryset().first(*args, **kwargs)

    def latest(self) -> QuerySet[ModelType]:
        """
        Retrieve the latest instance of the model.

        This method returns a new `QuerySet` instance that includes the latest
        instance of the model class defined in the `model` attribute of the manager.

        Returns:
            QuerySet[ModelType]: A new `QuerySet` instance containing the latest instance of the associated model.
        """
        return self.get_queryset().latest()

    def previous_version(self, obj: ModelType) -> ModelType | None:
        """
        Retrieve the previous version of the given model instance.

        This method returns the previous version of the specified model instance
        by querying the database for the instance with the prior version number.
        If no prior version exists, None is returned.

        Args:
            obj (ModelType): The model instance for which to retrieve the previous version.

        Returns:
            ModelType | None: The previous version of the model instance, or None if no prior version exists.
        """
        object_id = obj.object_id
        object_version = obj.get_metadata().prior_version

        if not object_version:
            return None

        q = Q(_address__object_version=object_version)

        return self.get_queryset().using(LAKEHOUSE_DB_ALIAS).first(q, _address__object_id=object_id).execute()

    async def aprevious_version(self, obj: ModelType) -> ModelType | None:
        """
        Retrieve the previous version of the given model instance.

        This method returns the previous version of the specified model instance
        by querying the database for the instance with the prior version number.
        If no prior version exists, None is returned.

        Args:
            obj (ModelType): The model instance for which to retrieve the previous version.

        Returns:
            ModelType | None: The previous version of the model instance, or None if no prior version exists.
        """
        object_id = obj.object_id
        object_version = (await obj.aget_metadata()).prior_version

        if not object_version:
            return None

        q = Q(_address__object_version=object_version)

        return await self.get_queryset().using(LAKEHOUSE_DB_ALIAS).first(q, _address__object_id=object_id).aexecute()

    def next_version(self, obj: ModelType) -> ModelType | None:
        """
        Retrieve the next version of the given model instance.

        This method returns the next version of the specified model instance
        by querying the database for the instance with the next version number.
        If no next version exists, None is returned.

        Args:
            obj (ModelType): The model instance for which to retrieve the next version.

        Returns:
            ModelType | None: The next version of the model instance, or None if no next version exists.
        """
        object_id = obj.object_id
        object_version = obj.get_metadata().next_version

        return self.get_specific_version(object_id, object_version)

    async def anext_version(self, obj: ModelType) -> ModelType | None:
        """
        Retrieve the next version of the given model instance.

        This method returns the next version of the specified model instance
        by querying the database for the instance with the next version number.
        If no next version exists, None is returned.

        Args:
            obj (ModelType): The model instance for which to retrieve the next version.

        Returns:
            ModelType | None: The next version of the model instance, or None if no next version exists.
        """
        object_id = obj.object_id
        object_version = (await obj.aget_metadata()).next_version

        return await self.aget_specific_version(object_id, object_version)

    def get_specific_version(self, object_id: str, object_version: str | None) -> ModelType | None:
        """
        Retrieve a specific version of the model instance.

        This method returns a specific version of the model instance identified by
        the given `object_id` and `object_version`. If the `object_version` is not
        provided, None is returned. The method queries the database using the
        `LAKEHOUSE_DB_ALIAS` to find the instance with the specified version.

        Args:
            object_id (str): The unique identifier of the model instance.
            object_version (str | None): The version number of the model instance.

        Returns:
            ModelType | None: The model instance with the specified version, or None if
            the `object_version` is not provided or no matching instance is found.
        """
        if not object_version:
            return None

        return (
            self.get_queryset()
            .using(LAKEHOUSE_DB_ALIAS)
            .get(
                _address__class_version=Versions.ALL,
                _address__object_id=object_id,
                _address__object_version=object_version,
            )
            .execute()
        )

    async def aget_specific_version(self, object_id: str, object_version: str | None) -> ModelType | None:
        """
        Retrieve a specific version of the model instance.

        This method returns a specific version of the model instance identified by
        the given `object_id` and `object_version`. If the `object_version` is not
        provided, None is returned. The method queries the database using the
        `LAKEHOUSE_DB_ALIAS` to find the instance with the specified version.

        Args:
            object_id (str): The unique identifier of the model instance.
            object_version (str | None): The version number of the model instance.

        Returns:
            ModelType | None: The model instance with the specified version, or None if
            the `object_version` is not provided or no matching instance is found.
        """
        if not object_version:
            return None

        return await (
            self.get_queryset()
            .using(LAKEHOUSE_DB_ALIAS)
            .get(
                _address__class_version=Versions.ALL,
                _address__object_id=object_id,
                _address__object_version=object_version,
            )
            .aexecute()
        )

    @transaction
    def bulk_create(self, objs: list[ModelType], using: str | None = None) -> None:
        """
        Perform a bulk update on the given list of model instances.

        This method updates multiple instances of the model class defined in the
        `model` attribute of the manager in a single query. The `using` parameter
        allows specifying a database alias for the operation.

        Args:
            objs (list[ModelType]): A list of model instances to be updated.
            using (str | None): The database alias to be used for the bulk update operation.
            If None, the default database alias is used.

        Returns:
            None
        """
        from amsdal_data.application import DataApplication

        for obj in objs:
            if not obj.is_new_object:
                msg = 'Cannot create some objects: some are already saved'
                raise BulkOperationError(msg)

            if not isinstance(obj, self.model):
                msg = 'Cannot apply a bulk operation on objects of different types'
                raise BulkOperationError(msg)

        operation_manager = DataApplication().operation_manager

        command = glue.DataCommand(
            root_transaction_id=self._transaction_manager.get_root_transaction_id(),
            transaction_id=self._transaction_manager.transaction_id,
            mutations=[
                glue.InsertData(
                    schema=glue.SchemaReference(
                        name=self.model.__name__,
                        version=(HistoricalSchemaVersionManager().get_latest_schema_version(self.model.__name__)),
                    ),
                    data=[model_to_data(obj) for obj in objs],
                ),
            ],
        )

        if using == LAKEHOUSE_DB_ALIAS:
            result = operation_manager.perform_data_command_lakehouse(command)
        else:
            result = operation_manager.perform_data_command(command)

        if not result.success:
            msg = f'Bulk create operation failed: {result.message}'
            raise BulkOperationError(msg) from result.exception

    @async_transaction
    async def bulk_acreate(self, objs: list[ModelType], using: str | None = None) -> None:
        """
        Perform a bulk update on the given list of model instances.

        This method updates multiple instances of the model class defined in the
        `model` attribute of the manager in a single query. The `using` parameter
        allows specifying a database alias for the operation.

        Args:
            objs (list[ModelType]): A list of model instances to be updated.
            using (str | None): The database alias to be used for the bulk update operation.
            If None, the default database alias is used.

        Returns:
            None
        """
        from amsdal_data.application import AsyncDataApplication

        for obj in objs:
            if not obj.is_new_object:
                msg = 'Cannot create some objects: some are already saved'
                raise BulkOperationError(msg)

            if not isinstance(obj, self.model):
                msg = 'Cannot apply a bulk operation on objects of different types'
                raise BulkOperationError(msg)

        operation_manager = AsyncDataApplication().operation_manager

        command = glue.DataCommand(
            root_transaction_id=AmsdalAsyncTransactionManager().get_root_transaction_id(),
            transaction_id=AmsdalAsyncTransactionManager().transaction_id,
            mutations=[
                glue.InsertData(
                    schema=glue.SchemaReference(
                        name=self.model.__name__,
                        version=(
                            await AsyncHistoricalSchemaVersionManager().get_latest_schema_version(self.model.__name__)
                        ),
                    ),
                    data=[model_to_data(obj) for obj in objs],
                ),
            ],
        )

        if using == LAKEHOUSE_DB_ALIAS:
            result = await operation_manager.perform_data_command_lakehouse(command)
        else:
            result = await operation_manager.perform_data_command(command)

        if not result.success:
            msg = f'Bulk create operation failed: {result.message}'
            raise BulkOperationError(msg) from result.exception

    @transaction
    def bulk_update(self, objs: list[ModelType], using: str | None = None) -> None:
        """
        Perform a bulk creation of the given list of model instances.

        This method creates multiple instances of the model class defined in the
        `model` attribute of the manager in a single query. The `using` parameter
        allows specifying a database alias for the operation.

        Args:
            objs (list[ModelType]): A list of model instances to be created.
            using (str | None): The database alias to be used for the bulk creation operation.
            If None, the default database alias is used.

        Returns:
            None
        """
        from amsdal_data.application import DataApplication

        for obj in objs:
            if obj.is_new_object:
                msg = 'Cannot update a new object'
                raise BulkOperationError(msg)

            if not obj.is_latest:
                msg = 'Cannot update an object that is not the latest version'
                raise BulkOperationError(msg)

            if not isinstance(obj, self.model):
                msg = 'Cannot apply a bulk operation on objects of different types'
                raise BulkOperationError(msg)

        operation_manager = DataApplication().operation_manager
        mutations: list[DataMutation] = []
        for obj in objs:
            if using == LAKEHOUSE_DB_ALIAS:
                query = glue.Conditions(
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=PRIMARY_PARTITION_KEY),
                            table_name=self.model.__name__,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(value=obj.object_id),
                    ),
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=SECONDARY_PARTITION_KEY),
                            table_name=self.model.__name__,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(value=obj.get_metadata().object_version),
                    ),
                )
            else:
                query = glue.Conditions(
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=PRIMARY_PARTITION_KEY),
                            table_name=self.model.__name__,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(value=obj.object_id),
                    ),
                )
            mutations.append(
                glue.UpdateData(
                    schema=glue.SchemaReference(
                        name=self.model.__name__,
                        version=(HistoricalSchemaVersionManager().get_latest_schema_version(self.model.__name__)),
                    ),
                    data=model_to_data(obj),
                    query=query,
                )
            )

        command = glue.DataCommand(
            root_transaction_id=self._transaction_manager.get_root_transaction_id(),
            transaction_id=self._transaction_manager.transaction_id,
            mutations=mutations,
        )

        if using == LAKEHOUSE_DB_ALIAS:
            result = operation_manager.perform_data_command_lakehouse(command)
        else:
            result = operation_manager.perform_data_command(command)

        if not result.success:
            msg = 'Bulk update operation failed'
            raise BulkOperationError(msg) from result.exception

    @async_transaction
    async def bulk_aupdate(self, objs: list[ModelType], using: str | None = None) -> None:
        """
        Perform a bulk creation of the given list of model instances.

        This method creates multiple instances of the model class defined in the
        `model` attribute of the manager in a single query. The `using` parameter
        allows specifying a database alias for the operation.

        Args:
            objs (list[ModelType]): A list of model instances to be created.
            using (str | None): The database alias to be used for the bulk creation operation.
            If None, the default database alias is used.

        Returns:
            None
        """
        from amsdal_data.application import AsyncDataApplication

        for obj in objs:
            if obj.is_new_object:
                msg = 'Cannot update a new object'
                raise BulkOperationError(msg)

            if not obj.is_latest:
                msg = 'Cannot update an object that is not the latest version'
                raise BulkOperationError(msg)

            if not isinstance(obj, self.model):
                msg = 'Cannot apply a bulk operation on objects of different types'
                raise BulkOperationError(msg)

        operation_manager = AsyncDataApplication().operation_manager
        mutations: list[DataMutation] = []
        for obj in objs:
            if using == LAKEHOUSE_DB_ALIAS:
                query = glue.Conditions(
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=PRIMARY_PARTITION_KEY),
                            table_name=self.model.__name__,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(value=(await obj.aget_metadata()).address.object_id),
                    ),
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=SECONDARY_PARTITION_KEY),
                            table_name=self.model.__name__,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(value=(await obj.aget_metadata()).address.object_version),
                    ),
                )
            else:
                query = glue.Conditions(
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=PRIMARY_PARTITION_KEY),
                            table_name=self.model.__name__,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(value=(await obj.aget_metadata()).address.object_id),
                    ),
                )
            mutations.append(
                glue.UpdateData(
                    schema=glue.SchemaReference(
                        name=self.model.__name__,
                        version=(
                            await AsyncHistoricalSchemaVersionManager().get_latest_schema_version(self.model.__name__)
                        ),
                    ),
                    data=model_to_data(obj),
                    query=query,
                )
            )

        command = glue.DataCommand(
            root_transaction_id=AmsdalAsyncTransactionManager().get_root_transaction_id(),
            transaction_id=AmsdalAsyncTransactionManager().transaction_id,
            mutations=mutations,
        )

        if using == LAKEHOUSE_DB_ALIAS:
            result = await operation_manager.perform_data_command_lakehouse(command)
        else:
            result = await operation_manager.perform_data_command(command)

        if not result.success:
            msg = 'Bulk update operation failed'
            raise BulkOperationError(msg) from result.exception

    @transaction
    def bulk_delete(self, objs: list[ModelType], using: str | None = None) -> None:
        """
        Perform a bulk deletion of the given list of model instances.

        This method deletes multiple instances of the model class defined in the
        `model` attribute of the manager in a single query. The `using` parameter
        allows specifying a database alias for the operation.

        Args:
            objs (list[ModelType]): A list of model instances to be deleted.
            using (str | None): The database alias to be used for the bulk deletion operation.
            If None, the default database alias is used.

        Returns:
            None
        """
        from amsdal_data.application import DataApplication

        for obj in objs:
            if obj.is_new_object:
                msg = 'Cannot delete a new object'
                raise BulkOperationError(msg)

            if not obj.is_latest:
                msg = 'Cannot delete an object that is not the latest version'
                raise BulkOperationError(msg)

            if not isinstance(obj, self.model):
                msg = 'Cannot apply a bulk operation on objects of different types'
                raise BulkOperationError(msg)

        operation_manager = DataApplication().operation_manager

        mutations: list[DataMutation] = []

        for obj in objs:
            mutation = glue.DeleteData(
                schema=glue.SchemaReference(
                    name=self.model.__name__,
                    version=(HistoricalSchemaVersionManager().get_latest_schema_version(self.model.__name__)),
                ),
                query=glue.Conditions(
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=PRIMARY_PARTITION_KEY),
                            table_name=self.model.__name__,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(value=obj.object_id),
                    ),
                ),
            )

            mutations.append(mutation)

            if using != LAKEHOUSE_DB_ALIAS and not DataApplication().is_lakehouse_only:
                continue

            if obj.get_metadata().is_latest:
                if mutation.query:
                    _next_version_field = glue.FieldReference(
                        field=glue.Field(name=NEXT_VERSION_FIELD),
                        table_name=METADATA_TABLE_ALIAS,
                    )
                    mutation.query &= glue.Conditions(
                        glue.Condition(
                            field=_next_version_field,
                            lookup=glue.FieldLookup.ISNULL,
                            value=glue.Value(value=True),
                        ),
                        glue.Condition(
                            field=_next_version_field,
                            lookup=glue.FieldLookup.EQ,
                            value=glue.Value(value=''),
                        ),
                        connector=glue.FilterConnector.OR,
                    )
            else:
                _object_version = obj.get_metadata().object_version
                msg = f'Invalid object version: {_object_version}. Delete not latest version is not allowed'
                raise BulkOperationError(msg)

        command = glue.DataCommand(
            mutations=mutations,
            root_transaction_id=self._transaction_manager.get_root_transaction_id(),
            transaction_id=self._transaction_manager.transaction_id,
        )

        if using == LAKEHOUSE_DB_ALIAS:
            result = operation_manager.perform_data_command_lakehouse(command)
        else:
            result = operation_manager.perform_data_command(command)

        if not result.success:
            msg = 'Bulk delete operation failed'
            raise BulkOperationError(msg) from result.exception

    @async_transaction
    async def bulk_adelete(self, objs: list[ModelType], using: str | None = None) -> None:
        """
        Perform a bulk deletion of the given list of model instances.

        This method deletes multiple instances of the model class defined in the
        `model` attribute of the manager in a single query. The `using` parameter
        allows specifying a database alias for the operation.

        Args:
            objs (list[ModelType]): A list of model instances to be deleted.
            using (str | None): The database alias to be used for the bulk deletion operation.
            If None, the default database alias is used.

        Returns:
            None
        """
        from amsdal_data.application import AsyncDataApplication

        for obj in objs:
            if obj.is_new_object:
                msg = 'Cannot delete a new object'
                raise BulkOperationError(msg)

            if not obj.is_latest:
                msg = 'Cannot delete an object that is not the latest version'
                raise BulkOperationError(msg)

            if not isinstance(obj, self.model):
                msg = 'Cannot apply a bulk operation on objects of different types'
                raise BulkOperationError(msg)

        operation_manager = AsyncDataApplication().operation_manager

        mutations: list[DataMutation] = []

        for obj in objs:
            mutation = glue.DeleteData(
                schema=glue.SchemaReference(
                    name=self.model.__name__,
                    version=(
                        await AsyncHistoricalSchemaVersionManager().get_latest_schema_version(self.model.__name__)
                    ),
                ),
                query=glue.Conditions(
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=PRIMARY_PARTITION_KEY),
                            table_name=self.model.__name__,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(value=obj.object_id),
                    ),
                ),
            )
            mutations.append(mutation)

            if using != LAKEHOUSE_DB_ALIAS and not AsyncDataApplication().is_lakehouse_only:
                continue

            if (await obj.aget_metadata()).is_latest:
                if mutation.query:
                    _next_version_field = glue.FieldReference(
                        field=glue.Field(name=NEXT_VERSION_FIELD),
                        table_name=METADATA_TABLE_ALIAS,
                    )
                    mutation.query &= glue.Conditions(
                        glue.Condition(
                            field=_next_version_field,
                            lookup=glue.FieldLookup.ISNULL,
                            value=glue.Value(value=True),
                        ),
                        glue.Condition(
                            field=_next_version_field,
                            lookup=glue.FieldLookup.EQ,
                            value=glue.Value(value=''),
                        ),
                        connector=glue.FilterConnector.OR,
                    )
            else:
                _object_version = (await obj.aget_metadata()).object_version
                msg = f'Invalid object version: {_object_version}. Delete not latest version is not allowed'
                raise BulkOperationError(msg)

        command = glue.DataCommand(
            mutations=mutations,
            root_transaction_id=AmsdalAsyncTransactionManager().get_root_transaction_id(),
            transaction_id=AmsdalAsyncTransactionManager().transaction_id,
        )

        if using == LAKEHOUSE_DB_ALIAS:
            result = await operation_manager.perform_data_command_lakehouse(command)
        else:
            result = await operation_manager.perform_data_command(command)

        if not result.success:
            msg = 'Bulk delete operation failed'
            raise BulkOperationError(msg) from result.exception
