from amsdal_utils.errors import AmsdalError
from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.enums import SchemaTypes


class AmsdalUniquenessError(AmsdalError): ...


class ObjectAlreadyExistsError(AmsdalError):
    def __init__(self, address: Address) -> None:
        self.address = address


class AmsdalRecursionError(AmsdalError): ...


class AmsdalClassError(AmsdalError): ...


class AmsdalClassNotFoundError(AmsdalClassError):
    def __init__(self, model_name: str, schema_type: SchemaTypes):
        self.model_name = model_name
        self.schema_type = schema_type
