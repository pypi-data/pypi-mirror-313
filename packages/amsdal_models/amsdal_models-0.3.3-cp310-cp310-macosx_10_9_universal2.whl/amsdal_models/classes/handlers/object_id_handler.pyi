from _typeshed import Incomplete
from amsdal_models.classes.decorators.private_property import PrivateProperty as PrivateProperty
from amsdal_models.classes.handlers.metadata_handler import MetadataHandler as MetadataHandler
from typing import Any

logger: Incomplete

class ObjectIdHandler(MetadataHandler):
    _object_id: str
    _is_new_object: bool
    def __init__(self, **kwargs: Any) -> None: ...
    def object_id(self) -> str:
        """
        Object identifier. This is a unique identifier for the record. This is a UUID.

        Returns:
            str: UUID string of the object ID.
        """
    @object_id.setter
    def object_id_setter(self, object_id: str) -> None:
        """
        Set the object ID.

        Args:
            object_id (str): Object identifier.
        """
    def is_new_object(self) -> bool:
        """
        Returns True if the object is new and has not been saved to the database.

        Returns:
            bool: Boolean flag indicating if the object is new.
        """
