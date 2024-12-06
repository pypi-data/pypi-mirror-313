from amsdal_utils.models.base import ModelBase
from amsdal_utils.models.enums import SchemaTypes as SchemaTypes
from typing import ClassVar

class BaseModel(ModelBase):
    """
    Base model class that extends the ModelBase class.

    Attributes:
        schema_type (ClassVar[SchemaTypes]): The schema type of the model.
        class_fingerprint (ClassVar[str]): The fingerprint of the class.
    """
    schema_type: ClassVar[SchemaTypes]
    class_fingerprint: ClassVar[str]
