from amsdal_utils.models.data_models.schema import ObjectSchema as ObjectSchema
from enum import Enum

class CoreModules(str, Enum):
    """
    Enumeration for core modules.

    Attributes:
        REFERENCE (str): Represents the 'Reference' core module.
    """
    REFERENCE: str

class SystemModules(str, Enum):
    """
    Enumeration for system modules.

    Attributes:
        DICT (str): Represents the 'dict' system module.
        LIST (str): Represents the 'list' system module.
        ANY (str): Represents the 'Any' system module.
        TYPE (str): Represents the 'type' system module.
        OPTIONAL (str): Represents the 'Optional' system module.
        UNION (str): Represents the 'Union' system module.
        CLASS_VAR (str): Represents the 'ClassVar' system module.
        FIELD_VALIDATOR (str): Represents the 'field_validator' system module.
        FIELD_DICTIONARY_VALIDATOR (str): Represents the 'validate_non_empty_keys' system module.
        FIELD_OPTIONS_VALIDATOR (str): Represents the 'validate_options' system module.
        DATE (str): Represents the 'date' system module.
        DATETIME (str): Represents the 'datetime' system module.
    """
    DICT: str
    LIST: str
    ANY: str
    TYPE: str
    OPTIONAL: str
    UNION: str
    CLASS_VAR: str
    FIELD_VALIDATOR: str
    FIELD_DICTIONARY_VALIDATOR: str
    FIELD_OPTIONS_VALIDATOR: str
    DATE: str
    DATETIME: str

class ModelType(str, Enum):
    """
    Enumeration for model types.

    Attributes:
        TYPE (str): Represents the 'type' model type.
        MODEL (str): Represents the 'model' model type.
    """
    TYPE: str
    MODEL: str
    @classmethod
    def from_schema(cls, schema: ObjectSchema) -> ModelType:
        """
        Determines the model type from the given schema.

        Args:
            schema (ObjectSchema): The schema to determine the model type from.

        Returns:
            ModelType: The determined model type.
        """
