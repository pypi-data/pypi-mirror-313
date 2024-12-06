from typing import Any

from amsdal_data.aliases.using import LAKEHOUSE_DB_ALIAS
from amsdal_utils.models.data_models.enums import BaseClasses
from amsdal_utils.models.data_models.enums import MetaClasses
from amsdal_utils.models.data_models.schema import ObjectSchema
from amsdal_utils.models.enums import SchemaTypes
from pydantic import BaseModel
from pydantic import Field

from amsdal_models.schemas.manager import BuildSchemasManager


class DependencyModelNames(BaseModel):
    type_model_names: list[str] = Field(default_factory=list)
    core_model_names: list[str] = Field(default_factory=list)
    contrib_model_names: list[str] = Field(default_factory=list)
    user_model_names: list[str] = Field(default_factory=list)
    reference_model_names: list[str] = Field(default_factory=list)

    @classmethod
    def build_from_schemas_manager(cls, schemas_manager: BuildSchemasManager) -> 'DependencyModelNames':
        """
        Builds DependencyModelNames from a schemas manager.

        Args:
            schemas_manager (BuildSchemasManager): The schemas manager.

        Returns:
            DependencyModelNames: The built DependencyModelNames instance.
        """
        return cls(
            type_model_names=[schema.title for schema in schemas_manager.type_schemas],
            core_model_names=[schema.title for schema in schemas_manager.core_schemas],
            contrib_model_names=[schema.title for schema in schemas_manager.contrib_schemas],
            user_model_names=[schema.title for schema in schemas_manager.user_schemas],
            reference_model_names=[
                *[
                    _schema.title
                    for _schema in schemas_manager.core_schemas
                    if _schema.meta_class == MetaClasses.CLASS_OBJECT.value
                ],
                *[
                    _schema.title
                    for _schema in schemas_manager.contrib_schemas
                    if _schema.meta_class == MetaClasses.CLASS_OBJECT.value
                ],
                *[
                    _schema.title
                    for _schema in schemas_manager.user_schemas
                    if _schema.meta_class == MetaClasses.CLASS_OBJECT.value
                ],
            ],
        )

    @classmethod
    def build_from_database(cls) -> 'DependencyModelNames':
        """
        Builds DependencyModelNames from the database.

        Returns:
            DependencyModelNames: The built DependencyModelNames instance.
        """
        from amsdal_models.classes.helpers.reference_loader import ReferenceLoader
        from models.core.class_object_meta import ClassObjectMeta  # type: ignore[import-not-found]
        from models.type.object import Object  # type: ignore[import-not-found]

        objects = Object.objects.using(LAKEHOUSE_DB_ALIAS).latest().filter(_metadata__is_deleted=False).execute()
        class_objects = (
            ClassObjectMeta.objects.using(LAKEHOUSE_DB_ALIAS).latest().filter(_metadata__is_deleted=False).execute()
        )
        type_names = [obj.title for obj in objects if obj.title != BaseClasses.CLASS_OBJECT.value]
        core_names = [BaseClasses.CLASS_OBJECT.value]
        core_names.extend([obj.title for obj in class_objects if obj.class_schema_type == SchemaTypes.CORE.value])
        contrib_names = [obj.title for obj in class_objects if obj.class_schema_type == SchemaTypes.CONTRIB.value]
        user_names = [obj.title for obj in class_objects if obj.class_schema_type == SchemaTypes.USER.value]
        reference_model_names = []

        loaded_references = set()
        for meta_object in class_objects:
            class_object_reference = meta_object.get_metadata().class_meta_schema_reference
            if class_object_reference in loaded_references or class_object_reference is None:
                continue

            loaded_references.add(class_object_reference)

            class_object = ReferenceLoader(class_object_reference).load_reference(using=LAKEHOUSE_DB_ALIAS)

            dump = meta_object.model_dump()
            dump.update(class_object.model_dump())
            object_schema = ObjectSchema(**dump)

            if object_schema.meta_class == MetaClasses.CLASS_OBJECT.value:
                reference_model_names.append(meta_object.title)

        return cls(
            type_model_names=type_names,
            core_model_names=core_names,
            contrib_model_names=contrib_names,
            user_model_names=user_names,
            reference_model_names=reference_model_names,
        )


class DependencyItem(BaseModel):
    module: tuple[str | None, str, str | None]

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, DependencyItem):
            return self.module == other.module
        return False

    def __hash__(self) -> int:
        return hash(self.module)
