from _typeshed import Incomplete
from collections.abc import Iterator
from pathlib import Path
from pydantic import BaseModel as BaseModel

logger: Incomplete

def load_object_schema_from_json_file(file_path: Path, model_cls: type[BaseModel]) -> Iterator[BaseModel]:
    """
    Loads object schema from a JSON file and yields instances of the given model class.

    This function reads the content of the specified JSON file and attempts to parse it. If the content is a list,
    it yields instances of the given model class for each item in the list. Otherwise, it yields a single instance
    of the model class.

    Args:
        file_path (Path): The path to the JSON file containing the data.
        model_cls (type[BaseModel]): The Pydantic model class to validate and instantiate the data.

    Yields:
        Iterator[BaseModel]: An iterator over instances of the model class created from the JSON data.

    Raises:
        json.JSONDecodeError: If the JSON file cannot be decoded.
    """
