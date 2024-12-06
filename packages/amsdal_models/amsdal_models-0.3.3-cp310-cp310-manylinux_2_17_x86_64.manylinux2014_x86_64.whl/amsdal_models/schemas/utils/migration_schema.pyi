from amsdal_models.classes.model import Model as Model
from amsdal_utils.models.data_models.schema import ObjectSchema as ObjectSchema, PropertyData as PropertyData
from amsdal_utils.models.data_models.table_schema import TableColumnSchema, TableSchema

def object_schema_to_table_schema(object_schema: ObjectSchema) -> TableSchema:
    """
    Converts an ObjectSchema to a TableSchema.

    Args:
        object_schema (ObjectSchema): The ObjectSchema object to convert.

    Returns:
        TableSchema: The converted TableSchema object.
    """
def _process_properties(properties: dict[str, PropertyData] | None, required: list[str]) -> list[TableColumnSchema]: ...
def _process_property_type(property_type: str) -> type | Model: ...
