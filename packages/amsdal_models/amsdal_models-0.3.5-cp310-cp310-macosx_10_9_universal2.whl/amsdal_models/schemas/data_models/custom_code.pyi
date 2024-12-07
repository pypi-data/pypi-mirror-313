from pydantic import BaseModel, Field as Field
from typing import Annotated

class CustomCodeSchema(BaseModel):
    """
    Schema for custom code.

    This class represents the schema for custom code, including the name and the code itself.

    Attributes:
        name (Annotated[str, Field]): The name of the custom code,
            with a minimum length of 1 and a maximum length of 255.
        code (str): The custom code as a string.
    """
    name: Annotated[str, None]
    code: str
    @property
    def property_names(self) -> list[str]:
        """
        Extract property names from the custom code.

        This method uses a regular expression to find all property names defined
        in the custom code string.

        Returns:
            list[str]: A list of property names found in the custom code.
        """
