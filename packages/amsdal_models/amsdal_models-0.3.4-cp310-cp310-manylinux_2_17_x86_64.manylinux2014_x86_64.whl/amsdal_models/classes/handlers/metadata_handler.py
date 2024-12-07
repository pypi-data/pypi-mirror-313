import logging
from functools import partial
from typing import Any
from typing import ClassVar

import amsdal_glue as glue
from amsdal_data.application import AsyncDataApplication
from amsdal_data.application import DataApplication
from amsdal_data.connections.historical.metadata_query import build_metadata_query
from amsdal_utils.models.data_models.enums import BaseClasses
from amsdal_utils.models.data_models.metadata import Metadata
from amsdal_utils.models.enums import Versions
from amsdal_utils.utils.lazy_object import LazyObject
from pydantic import PrivateAttr

from amsdal_models.classes.base import BaseModel
from amsdal_models.classes.constants import PARTIAL_CLASS_NAME_SUFFIX
from amsdal_models.classes.decorators.private_property import PrivateProperty
from amsdal_models.classes.utils import build_class_meta_schema_reference
from amsdal_models.classes.utils import build_class_schema_reference
from amsdal_models.classes.utils import is_partial_model

logger = logging.getLogger(__name__)


class MetadataHandler(BaseModel):
    _class_address: ClassVar[str]

    _object_id: str = PrivateAttr()
    _is_from_lakehouse: bool = PrivateAttr(default=False)
    _metadata_lazy: LazyObject[Metadata] = PrivateAttr()

    def __init__(self, **kwargs: Any):
        metadata = kwargs.pop('_metadata', None)
        super().__init__(**kwargs)

        self._metadata_lazy = LazyObject(partial(self.build_metadata, metadata=metadata))

    @PrivateProperty
    def _metadata(self) -> Metadata:
        return self._metadata_lazy.value

    @PrivateProperty
    def is_latest(self) -> bool:
        return self._metadata.is_latest

    @PrivateProperty
    def is_from_lakehouse(self) -> bool:
        return self._is_from_lakehouse

    def build_metadata(self, metadata: dict[str, Any] | Metadata | None) -> Metadata:
        """
        Builds the metadata object for this record.

        Returns:
            Metadata: The metadata object for this record.
        """
        if metadata:
            _metadata = metadata if isinstance(metadata, Metadata) else Metadata(**metadata)

            if _metadata.object_version != Versions.LATEST:
                self._is_from_lakehouse = True

            return _metadata

        class_name = self.__class__.__name__

        if is_partial_model(self.__class__) and class_name.endswith(PARTIAL_CLASS_NAME_SUFFIX):
            class_name = class_name[slice(0, -len(PARTIAL_CLASS_NAME_SUFFIX))]

        return Metadata(
            object_id=self._object_id,
            object_version=Versions.LATEST,
            class_schema_reference=build_class_schema_reference(class_name, self.__class__),
            class_meta_schema_reference=build_class_meta_schema_reference(class_name, self._object_id),
            class_schema_type=self.schema_type,
        )

    def get_metadata(self) -> Metadata:
        """
        Returns the metadata object for this record.

        Returns:
            Metadata: The metadata object for this record.
        """
        if self._metadata.object_version == Versions.LATEST:
            query = build_metadata_query(
                object_id=self._object_id,
                is_class_meta=self.__class__ == BaseClasses.CLASS_OBJECT_META,
            )
            query.limit = glue.LimitQuery(limit=1, offset=0)
            result = DataApplication().operation_manager.query_lakehouse(query)

            if not result.success:
                msg = f'Failed to retrieve metadata for object_id: {self._object_id}'
                raise ValueError(msg) from result.exception

            if not result.data:
                msg = f'No metadata found for object_id: {self._object_id}. Make sure the object was saved.'
                raise ValueError(msg) from None

            self._metadata_lazy = LazyObject(
                lambda: Metadata(**result.data[0].data),  # type: ignore[index]
            )

        return self._metadata

    async def aget_metadata(self) -> Metadata:
        """
        Returns the metadata object for this record.

        Returns:
            Metadata: The metadata object for this record.
        """
        if self._metadata.object_version == Versions.LATEST:
            query = build_metadata_query(
                object_id=self._object_id,
                is_class_meta=self.__class__ == BaseClasses.CLASS_OBJECT_META,
            )
            query.limit = glue.LimitQuery(limit=1, offset=0)

            result = await AsyncDataApplication().operation_manager.query_lakehouse(query)

            if not result.success:
                msg = f'Failed to retrieve metadata for object_id: {self._object_id}'
                raise ValueError(msg) from result.exception

            if not result.data:
                msg = f'No metadata found for object_id: {self._object_id}. Make sure the object was saved.'
                raise ValueError(msg) from None

            self._metadata_lazy = LazyObject(
                lambda: Metadata(**result.data[0].data),  # type: ignore[index]
            )

        return self._metadata

    def _invalidate_metadata(self) -> None:
        self._metadata_lazy = LazyObject(partial(self.build_metadata, metadata=None))
