from amsdal_models.errors import AmsdalValidationError as AmsdalValidationError
from amsdal_models.schemas.utils.merger import merge_schema as merge_schema
from amsdal_utils.models.data_models.schema import ObjectSchema
from typing import Any

class EnrichSchemasMixin:
    """
    Mixin class to enrich schemas with additional configurations.

    This class provides methods to enrich type, core, contrib, and user schemas by merging them with additional
    configurations. It ensures that schemas are enriched in the correct order and raises an `AmsdalValidationError`
    if any parent schemas are missing.
    """
    def enrich_configs(self, type_schemas: list[ObjectSchema], core_schemas: list[ObjectSchema], contrib_schemas: list[ObjectSchema], user_schemas: list[ObjectSchema]) -> tuple[list[ObjectSchema], list[ObjectSchema], list[ObjectSchema], list[ObjectSchema]]:
        """
        Enriches the provided schemas with additional configurations.

        This method enriches type, core, contrib, and user schemas by merging them with additional configurations.
        It ensures that schemas are enriched in the correct order and raises an `AmsdalValidationError` if any parent
        schemas are missing.

        Args:
            type_schemas (list[ObjectSchema]): A list of type schemas to enrich.
            core_schemas (list[ObjectSchema]): A list of core schemas to enrich.
            contrib_schemas (list[ObjectSchema]): A list of contrib schemas to enrich.
            user_schemas (list[ObjectSchema]): A list of user schemas to enrich.

        Returns:
            tuple[list[ObjectSchema], list[ObjectSchema], list[ObjectSchema], list[ObjectSchema]]:
            A tuple containing the enriched type, core, contrib, and user schemas.

        Raises:
            AmsdalValidationError: If any parent schemas are missing.
        """
    def _enrich(self, type_schemas: list[ObjectSchema], schemas: list[ObjectSchema], extra_schemas: list[ObjectSchema] | None = ...) -> list[ObjectSchema]: ...
    @staticmethod
    def _decode_json(json_string: str) -> dict[str, Any]: ...
