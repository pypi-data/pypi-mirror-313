import typing_extensions
from amsdal_models.classes.constants import REFERENCE_FIELD_SUFFIX as REFERENCE_FIELD_SUFFIX
from amsdal_models.classes.handlers.object_id_handler import ObjectIdHandler as ObjectIdHandler
from amsdal_utils.models.data_models.reference import Reference
from typing import Any, Literal

IncEx: typing_extensions.TypeAlias

class ReferenceHandler(ObjectIdHandler):
    _serialize_with_refs: bool
    _exclude_none: bool
    def build_reference(self, *, is_frozen: bool = ...) -> Reference:
        """
        Reference of the object/record. It's always referenced to latest object version.

        Returns:
            Reference: The reference of the object/record.
        """
    async def abuild_reference(self, *, is_frozen: bool = ...) -> Reference:
        """
        Reference of the object/record. It's always referenced to latest object version.

        Returns:
            Reference: The reference of the object/record.
        """
    def ser_model(self) -> dict[str, Any]:
        """
        Serializes the model.

        Returns:
            dict[str, Any]: The serialized model as a dictionary.
        """
    def model_dump_refs(self, *, mode: Literal['json', 'python'] | str = ..., include: IncEx = ..., exclude: IncEx = ..., by_alias: bool = ..., context: Any | None = ..., exclude_unset: bool = ..., exclude_defaults: bool = ..., exclude_none: bool = ..., round_trip: bool = ..., warnings: bool = ..., serialize_as_any: bool = ...) -> dict[str, Any]:
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
    def model_dump(self, *, mode: Literal['json', 'python'] | str = ..., include: IncEx = ..., exclude: IncEx = ..., context: Any | None = ..., by_alias: bool = ..., exclude_unset: bool = ..., exclude_defaults: bool = ..., exclude_none: bool = ..., round_trip: bool = ..., warnings: bool = ..., serialize_as_any: bool = ...) -> dict[str, Any]:
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
    def model_dump_json_refs(self, *, indent: int | None = ..., include: IncEx = ..., exclude: IncEx = ..., context: Any | None = ..., by_alias: bool = ..., exclude_unset: bool = ..., exclude_defaults: bool = ..., exclude_none: bool = ..., round_trip: bool = ..., warnings: bool = ..., serialize_as_any: bool = ...) -> str:
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
    def model_dump_json(self, *, indent: int | None = ..., include: IncEx = ..., exclude: IncEx = ..., context: Any | None = ..., by_alias: bool = ..., exclude_unset: bool = ..., exclude_defaults: bool = ..., exclude_none: bool = ..., round_trip: bool = ..., warnings: bool = ..., serialize_as_any: bool = ...) -> str:
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
