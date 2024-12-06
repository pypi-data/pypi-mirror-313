from amsdal_utils.models.data_models.schema import ObjectSchema as ObjectSchema

def calculate_schema_fingerprint(schema: ObjectSchema) -> str:
    """
    Calculates the fingerprint of a given schema.

    This function takes an `ObjectSchema` and calculates its fingerprint using SHA-256 hashing. The schema is first
    serialized to a JSON string with sorted keys, and then the SHA-256 hash of this string is computed.

    Args:
        schema (ObjectSchema): The schema for which to calculate the fingerprint.

    Returns:
        str: The SHA-256 fingerprint of the schema.
    """
