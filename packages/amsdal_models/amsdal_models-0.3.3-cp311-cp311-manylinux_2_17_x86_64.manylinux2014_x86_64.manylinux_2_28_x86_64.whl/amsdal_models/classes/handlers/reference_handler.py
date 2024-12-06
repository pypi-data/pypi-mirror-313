from typing import Any
from typing import Literal

import typing_extensions
from amsdal_utils.config.manager import AmsdalConfigManager
from amsdal_utils.models.data_models.reference import Reference
from amsdal_utils.models.enums import Versions
from amsdal_utils.models.utils.reference_builders import build_reference
from pydantic import PrivateAttr
from pydantic import model_serializer

from amsdal_models.classes.constants import REFERENCE_FIELD_SUFFIX
from amsdal_models.classes.handlers.object_id_handler import ObjectIdHandler

# should be `set[int] | set[str] | dict[int, IncEx] | dict[str, IncEx] | None`, but mypy can't cope
IncEx: typing_extensions.TypeAlias = 'set[int] | set[str] | dict[int, Any] | dict[str, Any] | None'


class ReferenceHandler(ObjectIdHandler):
    _serialize_with_refs: bool = PrivateAttr(default=False)
    _exclude_none: bool = PrivateAttr(default=False)

    def build_reference(self, *, is_frozen: bool = False) -> Reference:
        """
        Reference of the object/record. It's always referenced to latest object version.

        Returns:
            Reference: The reference of the object/record.
        """
        from amsdal_utils.config.manager import AmsdalConfigManager

        if not is_frozen:
            return build_reference(
                resource=AmsdalConfigManager().get_connection_name_by_model_name(
                    self.__class__.__name__,
                ),
                class_name=self.__class__.__name__,
                class_version=Versions.LATEST,
                object_id=self.object_id,
                object_version=Versions.LATEST,
            )

        metadata = self.get_metadata()
        reference_address = metadata.address

        if reference_address.object_version == Versions.LATEST:
            msg = (
                'Cannot freeze the latest version of the object. Make sure you have saved the object first and '
                'you are using lakehouse connection.'
            )
            raise ValueError(msg)

        return build_reference(
            resource=reference_address.resource,
            class_name=reference_address.class_name,
            object_id=reference_address.object_id,
            class_version=reference_address.class_version,
            object_version=reference_address.object_version,
        )

    async def abuild_reference(self, *, is_frozen: bool = False) -> Reference:
        """
        Reference of the object/record. It's always referenced to latest object version.

        Returns:
            Reference: The reference of the object/record.
        """
        from amsdal_utils.config.manager import AmsdalConfigManager

        if not is_frozen:
            return build_reference(
                resource=AmsdalConfigManager().get_connection_name_by_model_name(
                    self.__class__.__name__,
                ),
                class_name=self.__class__.__name__,
                class_version=Versions.LATEST,
                object_id=self.object_id,
                object_version=Versions.LATEST,
            )

        metadata = await self.aget_metadata()
        reference_address = metadata.address

        if reference_address.object_version == Versions.LATEST:
            msg = (
                'Cannot freeze the latest version of the object. Make sure you have saved the object first and '
                'you are using lakehouse connection.'
            )
            raise ValueError(msg)

        return build_reference(
            resource=reference_address.resource,
            class_name=reference_address.class_name,
            object_id=reference_address.object_id,
            class_version=reference_address.class_version,
            object_version=reference_address.object_version,
        )

    @model_serializer
    def ser_model(self) -> dict[str, Any]:
        """
        Serializes the model.

        Returns:
            dict[str, Any]: The serialized model as a dictionary.
        """
        from amsdal_models.classes.base import BaseModel
        from amsdal_models.classes.helpers.reference_loader import ReferenceLoader
        from amsdal_models.classes.model import Model

        data: dict[str, Any] = {}
        stack_context = {
            id(self): data,
        }

        def _serialize_value(_value: Any, _stack_context: dict[Any, dict[str, Any]]) -> Any:
            _value_id = id(_value)
            ref_hash: int | None = None

            if _stack_context is not None and _value_id in _stack_context:
                return _stack_context[_value_id]

            if isinstance(_value, Reference):
                ref_hash = hash(_value)

                if _stack_context is not None and ref_hash in _stack_context:
                    return _stack_context[ref_hash]

                if self._serialize_with_refs:
                    _value = _value.model_dump(exclude_none=self._exclude_none)
                elif not AmsdalConfigManager().get_config().async_mode:
                    _value = ReferenceLoader(_value).load_reference()

                if _stack_context is not None:
                    _stack_context[ref_hash] = _value

            if isinstance(_value, BaseModel):
                if _stack_context is not None:
                    _stack_context[_value_id] = {}

                    if ref_hash is not None:
                        _stack_context[ref_hash] = _stack_context[_value_id]

                if self._serialize_with_refs and isinstance(_value, Model):
                    _value = _value.build_reference().model_dump(exclude_none=self._exclude_none)
                else:
                    _dict_value = {}

                    for _field in _value.model_fields:
                        _field_value = getattr(_value, _field)

                        if isinstance(_field_value, list):
                            _field_value = [_serialize_value(item, stack_context) for item in _field_value]
                        elif isinstance(_field_value, dict):
                            _field_value = {
                                key: _serialize_value(item, stack_context) for key, item in _field_value.items()
                            }

                        if _field_value is not None or not self._exclude_none:
                            _dict_value[_field] = _serialize_value(_field_value, stack_context)

                    _value = _dict_value

                if _stack_context is not None:
                    _stack_context[_value_id].update(_value)
            return _value

        # we want to save objects until we have serialized all fields because we might have ID collisions
        _mem = []

        for field_name in self.model_fields:
            _field_name = f'{field_name}{REFERENCE_FIELD_SUFFIX}' if self._serialize_with_refs else field_name
            value = getattr(self, _field_name)
            _mem.append(value)
            value = _serialize_value(value, stack_context)

            if isinstance(value, list):
                value = [_serialize_value(item, stack_context) for item in value]
            elif isinstance(value, dict):
                value = {key: _serialize_value(item, stack_context) for key, item in value.items()}

            if value is not None or not self._exclude_none:
                data[field_name] = value

        if self.__pydantic_extra__:
            for field_name, value in self.__pydantic_extra__.items():
                data[field_name] = value

        return data

    def model_dump_refs(
        self,
        *,
        mode: Literal['json', 'python'] | str = 'python',
        include: IncEx = None,
        exclude: IncEx = None,
        by_alias: bool = False,
        context: Any | None = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
        serialize_as_any: bool = False,
    ) -> dict[str, Any]:
        """
        Dumps the model with references.

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
            dict[str, Any]: The serialized model as a dictionary.
        """
        self._serialize_with_refs = True
        self._exclude_none = exclude_none
        return super(ObjectIdHandler, self).model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=serialize_as_any,
        )

    def model_dump(  # type: ignore[override]
        self,
        *,
        mode: Literal['json', 'python'] | str = 'python',
        include: IncEx = None,
        exclude: IncEx = None,
        context: Any | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
        serialize_as_any: bool = False,
    ) -> dict[str, Any]:
        """
        Dumps the model.

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
            dict[str, Any]: The serialized model as a dictionary.
        """
        self._serialize_with_refs = False
        self._exclude_none = exclude_none
        return super(ObjectIdHandler, self).model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=serialize_as_any,
        )

    def model_dump_json_refs(
        self,
        *,
        indent: int | None = None,
        include: IncEx = None,
        exclude: IncEx = None,
        context: Any | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
        serialize_as_any: bool = False,
    ) -> str:
        """
        Dumps the model as a JSON string with references.

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
            str: The serialized model as a JSON string.
        """
        self._serialize_with_refs = True
        self._exclude_none = exclude_none
        return super(ObjectIdHandler, self).model_dump_json(
            indent=indent,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=serialize_as_any,
        )

    def model_dump_json(  # type: ignore[override]
        self,
        *,
        indent: int | None = None,
        include: IncEx = None,
        exclude: IncEx = None,
        context: Any | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
        serialize_as_any: bool = False,
    ) -> str:
        """
        Dumps the model as a JSON string.

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
            str: The serialized model as a JSON string.
        """
        self._serialize_with_refs = False
        self._exclude_none = exclude_none
        return super(ObjectIdHandler, self).model_dump_json(
            indent=indent,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=serialize_as_any,
        )
