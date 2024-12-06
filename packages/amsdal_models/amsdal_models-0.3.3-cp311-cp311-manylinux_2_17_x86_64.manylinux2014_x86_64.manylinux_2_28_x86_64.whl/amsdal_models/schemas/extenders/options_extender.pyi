from _typeshed import Incomplete
from amsdal_models.errors import AmsdalValidationError as AmsdalValidationError
from amsdal_models.schemas.loaders.base import OptionsLoaderBase as OptionsLoaderBase
from amsdal_utils.models.data_models.schema import ObjectSchema as ObjectSchema

logger: Incomplete

class OptionsExtender:
    """
    Extends object schemas with options.

    This class is responsible for extending object schemas with options read from an options loader.
    """
    _options_reader: Incomplete
    _options: Incomplete
    _used_options: Incomplete
    def __init__(self, options_reader: OptionsLoaderBase) -> None: ...
    def extend(self, config: ObjectSchema) -> None:
        """
        Extends the given object schema with options if available.

        Args:
            config (ObjectSchema): The object schema to extend.

        Returns:
            None
        """
    def post_extend(self) -> None:
        """
        Logs any unused options lists.

        Returns:
            None
        """
