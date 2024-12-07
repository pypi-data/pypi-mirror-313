import json
import typing_extensions
from _typeshed import Incomplete
from amsdal_models.classes.base import BaseModel as BaseModel
from amsdal_models.classes.constants import REFERENCE_FIELD_SUFFIX as REFERENCE_FIELD_SUFFIX
from amsdal_models.classes.errors import AmsdalRecursionError as AmsdalRecursionError, AmsdalUniquenessError as AmsdalUniquenessError, ObjectAlreadyExistsError as ObjectAlreadyExistsError
from amsdal_models.classes.handlers.reference_handler import ReferenceHandler as ReferenceHandler
from amsdal_models.classes.mixins.model_hooks_mixin import ModelHooksMixin as ModelHooksMixin
from amsdal_models.classes.utils import is_partial_model as is_partial_model
from amsdal_models.managers.base_manager import BaseManager as BaseManager
from amsdal_models.querysets.errors import ObjectDoesNotExistError as ObjectDoesNotExistError
from amsdal_models.querysets.executor import DEFAULT_DB_ALIAS as DEFAULT_DB_ALIAS, LAKEHOUSE_DB_ALIAS as LAKEHOUSE_DB_ALIAS
from amsdal_utils.models.data_models.reference import Reference
from pydantic._internal._model_construction import ModelMetaclass
from typing import Any, ClassVar, Literal
from typing_extensions import Self

IncEx: typing_extensions.TypeAlias
logger: Incomplete

class TypeModel(ModelHooksMixin, ReferenceHandler, BaseModel):
    @classmethod
    def convert_string_to_dict(cls, data: Any) -> Any:
        """
        Converts a string to a dictionary if possible.

        Args:
            data (Any): The data to convert.

        Returns:
            Any: The converted data.
        """

class AmsdalModelMetaclass(ModelMetaclass):
    def __new__(mcs, cls_name: str, bases: tuple[type[Any], ...], namespace: dict[str, Any], *args: Any, **kwargs: Any) -> type: ...

class Model(TypeModel, metaclass=AmsdalModelMetaclass):
    """
    Base class for all model classes.

    Attributes:
        model_config (ConfigDict): Configuration for the model.
        objects (ClassVar[BaseManager[Self]]): Manager for the Model class.
    """
    _is_inside_save: bool
    model_config: Incomplete
    objects: ClassVar[BaseManager[Self]]
    def __init__(self, **kwargs: Any) -> None: ...
    _is_new_object: bool
    def save(self, *, force_insert: bool = ..., using: str | None = ..., skip_hooks: bool = ...) -> Self:
        """
        Saves the record of the Model object into the database.

        By default, the object will be updated in the database if it already exists.
        If `force_insert` is set to True, the object will be inserted into the database even if it already exists,
        which may result in an `ObjectAlreadyExistsError`.

        The method first checks if `force_insert` is True, and if the object already exists in the database.
        If it does, it raises an `ObjectAlreadyExistsError`.

        Then, depending on the object existence, the method either creates a new record in the database or updates
        the existing record. It also triggers the corresponding `pre_create()`, `post_create()`, `pre_update()`, and
        `post_update()` hooks.

        Finally, the method returns the saved Model object.

        Args:
            force_insert (bool): Indicates whether to force insert the object into the database,
            even if it already exists.
            using (str | None): The name of the database to use.
            skip_hooks (bool): Indicates whether to skip the hooks.

        Returns:
            Model: The saved Model object.
        """
    async def asave(self, *, force_insert: bool = ..., using: str | None = ..., skip_hooks: bool = ...) -> Self:
        """
        Saves the record of the Model object into the database.

        By default, the object will be updated in the database if it already exists.
        If `force_insert` is set to True, the object will be inserted into the database even if it already exists,
        which may result in an `ObjectAlreadyExistsError`.

        The method first checks if `force_insert` is True, and if the object already exists in the database.
        If it does, it raises an `ObjectAlreadyExistsError`.

        Then, depending on the object existence, the method either creates a new record in the database or updates
        the existing record. It also triggers the corresponding `pre_create()`, `post_create()`, `pre_update()`, and
        `post_update()` hooks.

        Finally, the method returns the saved Model object.

        Args:
            force_insert (bool): Indicates whether to force insert the object into the database,
            even if it already exists.
            using (str | None): The name of the database to use.
            skip_hooks (bool): Indicates whether to skip the hooks.

        Returns:
            Model: The saved Model object.
        """
    def delete(self, using: str | None = ..., *, skip_hooks: bool = ...) -> None:
        """
        Deletes the existing record of the Model object from the database.

        This method first calls the `pre_delete()` method, then deletes the record from the database by calling
            the `_delete()` method, and finally calls the `post_delete()` method.
        It changes the flag `is_deleted` to True in the metadata of the record.

        Args:
            using (str | None): The name of the database to use.
            skip_hooks (bool): Indicates whether to skip the `pre_delete()` and `post_delete()` hooks.

        Returns:
            None
        """
    async def adelete(self, using: str | None = ..., *, skip_hooks: bool = ...) -> None:
        """
        Deletes the existing record of the Model object from the database.

        This method first calls the `pre_delete()` method, then deletes the record from the database by calling
            the `_delete()` method, and finally calls the `post_delete()` method.
        It changes the flag `is_deleted` to True in the metadata of the record.

        Args:
            using (str | None): The name of the database to use.
            skip_hooks (bool): Indicates whether to skip the `pre_delete()` and `post_delete()` hooks.

        Returns:
            None
        """
    @property
    def display_name(self) -> str:
        """
        Gets the display name of the Model object.

        This method returns the string representation of the object's address.

        Returns:
            str: The display name of the Model object.
        """
    def _check_unique(self, using: str | None) -> None: ...
    async def _acheck_unique(self, using: str | None) -> None: ...
    def _create(self, using: str | None, *, skip_hooks: bool = ...) -> None: ...
    async def _acreate(self, using: str | None, *, skip_hooks: bool = ...) -> None: ...
    def _update(self, using: str | None, *, skip_hooks: bool = ...) -> None: ...
    async def _aupdate(self, using: str | None, *, skip_hooks: bool = ...) -> None: ...
    def _process_nested_objects(self) -> None: ...
    def _process_nested_field(self, field_value: Any) -> Any: ...
    async def _async_process_nested_objects(self) -> None: ...
    async def _async_process_nested_field(self, field_value: Any) -> Any: ...
    def model_dump_refs(self, *, mode: Literal['json', 'python'] | str = ..., include: IncEx = ..., exclude: IncEx = ..., context: Any | None = ..., by_alias: bool = ..., exclude_unset: bool = ..., exclude_defaults: bool = ..., exclude_none: bool = ..., round_trip: bool = ..., warnings: bool = ..., serialize_as_any: bool = ...) -> dict[str, Any]:
        """
        Dumps the record and its references into a dictionary of data.

        Args:
            mode (Literal['json', 'python'] | str, optional): The mode of serialization. Defaults to 'python'.
            include (IncEx, optional): Fields to include in the serialization. Defaults to None.
            exclude (IncEx, optional): Fields to exclude from the serialization. Defaults to None.
            context (Any | None, optional): The context of the serialization. Defaults to None.
            by_alias (bool, optional): Whether to use field aliases. Defaults to False.
            exclude_unset (bool, optional): Whether to exclude unset fields. Defaults to False.
            exclude_defaults (bool, optional): Whether to exclude fields with default values. Defaults to False.
            exclude_none (bool, optional): Whether to exclude fields with None values. Defaults to False.
            round_trip (bool, optional): Whether to ensure round-trip serialization. Defaults to False.
            warnings (bool, optional): Whether to show warnings. Defaults to True.
            serialize_as_any (bool, optional): Whether to serialize as Any. Defaults to False.

        Returns:
            dict[str, Any]: A dictionary representation of the model.
        """
    def model_dump(self, *, mode: Literal['json', 'python'] | str = ..., include: IncEx = ..., exclude: IncEx = ..., context: Any | None = ..., by_alias: bool = ..., exclude_unset: bool = ..., exclude_defaults: bool = ..., exclude_none: bool = ..., round_trip: bool = ..., warnings: bool = ..., serialize_as_any: bool = ...) -> dict[str, Any]:
        '''
        This method is used to dump the record dictionary of data, although the referenced objects will be represented
        in reference format. Here is an example of reference format:

            {
              "$ref": {
                "resource": "sqlite",
                "class_name": "Person",
                "class_version": "1234",
                "object_id": "4567",
                "object_version": "8901"
              }
            }

        Args:
            mode (Literal[\'json\', \'python\'] | str, optional): The mode of serialization. Defaults to \'python\'.
            include (IncEx, optional): Fields to include in the serialization. Defaults to None.
            exclude (IncEx, optional): Fields to exclude from the serialization. Defaults to None.
            context (Any | None, optional): The context of the serialization. Defaults to None.
            by_alias (bool, optional): Whether to use field aliases. Defaults to False.
            exclude_unset (bool, optional): Whether to exclude unset fields. Defaults to False.
            exclude_defaults (bool, optional): Whether to exclude fields with default values. Defaults to False.
            exclude_none (bool, optional): Whether to exclude fields with None values. Defaults to False.
            round_trip (bool, optional): Whether to ensure round-trip serialization. Defaults to False.
            warnings (bool, optional): Whether to show warnings. Defaults to True.
            serialize_as_any (bool, optional): Whether to serialize as Any. Defaults to False.

        Returns:
            dict[str, Any]: A dictionary representation of the model.
        '''
    def model_dump_json_refs(self, *, indent: int | None = ..., include: IncEx = ..., exclude: IncEx = ..., context: Any | None = ..., by_alias: bool = ..., exclude_unset: bool = ..., exclude_defaults: bool = ..., exclude_none: bool = ..., round_trip: bool = ..., warnings: bool = ..., serialize_as_any: bool = ...) -> str:
        """
        Similar to `model_dump_refs`, but returns a JSON string instead of a dictionary.

        Args:
            mode (Literal['json', 'python'] | str, optional): The mode of serialization. Defaults to 'python'.
            include (IncEx, optional): Fields to include in the serialization. Defaults to None.
            exclude (IncEx, optional): Fields to exclude from the serialization. Defaults to None.
            context (Any | None, optional): The context of the serialization. Defaults to None.
            by_alias (bool, optional): Whether to use field aliases. Defaults to False.
            exclude_unset (bool, optional): Whether to exclude unset fields. Defaults to False.
            exclude_defaults (bool, optional): Whether to exclude fields with default values. Defaults to False.
            exclude_none (bool, optional): Whether to exclude fields with None values. Defaults to False.
            round_trip (bool, optional): Whether to ensure round-trip serialization. Defaults to False.
            warnings (bool, optional): Whether to show warnings. Defaults to True.
            serialize_as_any (bool, optional): Whether to serialize as Any. Defaults to False.

        Returns:
            str: A JSON string representation of the model.
        """
    def model_dump_json(self, *, indent: int | None = ..., include: IncEx = ..., exclude: IncEx = ..., context: Any | None = ..., by_alias: bool = ..., exclude_unset: bool = ..., exclude_defaults: bool = ..., exclude_none: bool = ..., round_trip: bool = ..., warnings: bool = ..., serialize_as_any: bool = ...) -> str:
        """
        Similar to `model_dump`, but returns a JSON string instead of a dictionary.

        Args:
            mode (Literal['json', 'python'] | str, optional): The mode of serialization. Defaults to 'python'.
            include (IncEx, optional): Fields to include in the serialization. Defaults to None.
            exclude (IncEx, optional): Fields to exclude from the serialization. Defaults to None.
            context (Any | None, optional): The context of the serialization. Defaults to None.
            by_alias (bool, optional): Whether to use field aliases. Defaults to False.
            exclude_unset (bool, optional): Whether to exclude unset fields. Defaults to False.
            exclude_defaults (bool, optional): Whether to exclude fields with default values. Defaults to False.
            exclude_none (bool, optional): Whether to exclude fields with None values. Defaults to False.
            round_trip (bool, optional): Whether to ensure round-trip serialization. Defaults to False.
            warnings (bool, optional): Whether to show warnings. Defaults to True.
            serialize_as_any (bool, optional): Whether to serialize as Any. Defaults to False.

        Returns:
            str: A JSON string representation of the model.
        """
    def previous_version(self) -> Self | None:
        """
        Gets the previous version of the Model object from the database.

        This method returns the Model object that is the previous version of the current object, if it exists.
            Otherwise, it returns None.

        Returns:
            Self | None: The previous version of the Model object.
        """
    async def aprevious_version(self) -> Self | None:
        """
        Gets the previous version of the Model object from the database.

        This method returns the Model object that is the previous version of the current object, if it exists.
            Otherwise, it returns None.

        Returns:
            Self | None: The previous version of the Model object.
        """
    def next_version(self) -> Self | None:
        """
        Gets the next version of the Model object from the database.

        This method returns the Model object that is the next version of the current object, if it exists. Otherwise,
            it returns None.

        Returns:
            Self | None: The next version of the Model object.
        """
    async def anext_version(self) -> Self | None:
        """
        Gets the next version of the Model object from the database.

        This method returns the Model object that is the next version of the current object, if it exists. Otherwise,
            it returns None.

        Returns:
            Self | None: The next version of the Model object.
        """
    def refetch_from_db(self) -> Self:
        """
        Gets the object with the current version from the database.

        Returns:
            Self: The object with the current version from the database.
        """
    async def arefetch_from_db(self) -> Self:
        """
        Gets the object with the current version from the database.

        Returns:
            Self: The object with the current version from the database.
        """
    def __getattribute__(self, name: str) -> Any: ...
    @staticmethod
    async def _async_load_reference(ref: Reference) -> Any: ...
    def __eq__(self, other: Any) -> bool: ...
    def __neq__(self, other: Any) -> bool: ...

class LegacyModel(TypeModel, metaclass=AmsdalModelMetaclass):
    """
    LegacyModel class that inherits from TypeModel and uses AmsdalModelMetaclass as its metaclass.

    Attributes:
        model_config (ConfigDict): Configuration for the model.
    """
    model_config: Incomplete
