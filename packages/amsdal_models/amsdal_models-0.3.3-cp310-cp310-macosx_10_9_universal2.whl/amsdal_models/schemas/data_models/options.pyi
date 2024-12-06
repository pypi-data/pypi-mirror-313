from amsdal_utils.models.data_models.schema import OptionItemData as OptionItemData
from pydantic import BaseModel, Field as Field
from typing import Annotated

class OptionSchema(BaseModel):
    """
    Schema for an option.

    This class represents the schema for an option, including the title and the values.

    Attributes:
        title (Annotated[str, Field]): The title of the option, with a minimum length of 1 and a maximum length of 255.
        values (list[OptionItemData]): A list of option item data.
    """
    title: Annotated[str, None]
    values: list[OptionItemData]
