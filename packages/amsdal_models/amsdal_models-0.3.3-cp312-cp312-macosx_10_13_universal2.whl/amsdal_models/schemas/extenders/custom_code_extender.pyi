from _typeshed import Incomplete
from amsdal_models.schemas.loaders.base import CustomCodeLoaderBase as CustomCodeLoaderBase
from amsdal_utils.models.data_models.schema import ObjectSchema as ObjectSchema

logger: Incomplete

class CustomCodeExtender:
    """
    Extends object schemas with custom code.

    This class is responsible for extending object schemas with custom code read from a custom code loader.
    """
    _custom_code_reader: Incomplete
    _custom_code_schemas: Incomplete
    _used_custom_codes: Incomplete
    def __init__(self, custom_code_reader: CustomCodeLoaderBase) -> None: ...
    def extend(self, config: ObjectSchema) -> None:
        """
        Extends the given object schema with custom code if available.

        Args:
            config (ObjectSchema): The object schema to extend.

        Returns:
            None
        """
    def post_extend(self) -> None:
        """
        Logs any unused custom codes.
        """
