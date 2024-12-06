import logging
from typing import Any

from amsdal_utils.utils.identifier import get_identifier
from pydantic import PrivateAttr

from amsdal_models.classes.decorators.private_property import PrivateProperty
from amsdal_models.classes.handlers.metadata_handler import MetadataHandler

logger = logging.getLogger(__name__)


class ObjectIdHandler(MetadataHandler):
    _object_id: str = PrivateAttr()
    _is_new_object: bool = PrivateAttr(default=True)

    def __init__(self, **kwargs: Any):
        _object_id = kwargs.pop('_object_id', None)
        super().__init__(**kwargs)

        if _object_id is None:
            self._object_id = get_identifier()
            self._is_new_object = True
        else:
            self._object_id = _object_id
            self._is_new_object = False

    @PrivateProperty
    def object_id(self) -> str:
        """
        Object identifier. This is a unique identifier for the record. This is a UUID.

        Returns:
            str: UUID string of the object ID.
        """
        return self._object_id

    @object_id.setter
    def object_id_setter(self, object_id: str) -> None:
        """
        Set the object ID.

        Args:
            object_id (str): Object identifier.
        """
        self._object_id = object_id

    @PrivateProperty
    def is_new_object(self) -> bool:
        """
        Returns True if the object is new and has not been saved to the database.

        Returns:
            bool: Boolean flag indicating if the object is new.
        """
        return self._is_new_object
