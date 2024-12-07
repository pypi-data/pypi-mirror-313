from _typeshed import Incomplete
from amsdal_models.schemas.data_models.custom_code import CustomCodeSchema as CustomCodeSchema
from amsdal_models.schemas.loaders.base import ConfigReaderMixin as ConfigReaderMixin, CustomCodeLoaderBase as CustomCodeLoaderBase
from amsdal_utils.models.data_models.schema import ObjectSchema as ObjectSchema
from collections.abc import Iterator
from pathlib import Path

HOOKS: str
MODIFIERS: str
PROPERTIES: str
MODEL_JSON_FILE: str
logger: Incomplete

class CliCustomCodeLoader(ConfigReaderMixin, CustomCodeLoaderBase):
    """
    Loader for custom code in CLI.

    This class is responsible for loading custom code from a given schema directory. It extends the `ConfigReaderMixin`
    and `CustomCodeLoaderBase` to provide methods for iterating over custom code schemas and reading custom code from
    model directories and subdirectories.
    """
    _schema_dir: Incomplete
    def __init__(self, schema_dir: Path) -> None: ...
    def __str__(self) -> str: ...
    def iter_custom_code(self) -> Iterator[CustomCodeSchema]:
        """
        Iterates over custom code schemas.

        This method iterates over model directories and yields custom code schemas that contain code.

        Yields:
            CustomCodeSchema: The custom code schema containing the code.
        """
    def read_custom_code_from_model_directory(self, model_directory: Path, object_config: ObjectSchema) -> CustomCodeSchema:
        """
        Reads custom code from a model directory.

        This method reads custom code from the specified model directory by iterating over predefined subdirectories
        (hooks, modifiers, properties) and collecting Python code files.

        Args:
            model_directory (Path): The path to the model directory.
            object_config (ObjectSchema): The object schema configuration.

        Returns:
            CustomCodeSchema: The custom code schema containing the collected code.
        """
    def read_custom_code_from_subdirectory(self, model_directory: Path, subdirectory: str) -> list[str]:
        """
        Reads custom code from a subdirectory.

        This method reads Python code files from the specified subdirectory within the model directory. It collects the
        content of these files and returns them as a list of strings.

        Args:
            model_directory (Path): The path to the model directory.
            subdirectory (str): The name of the subdirectory to read code from.

        Returns:
            list[str]: A list of strings containing the content of the Python code files.
        """
    def iter_model_directories(self) -> Iterator[tuple[Path, ObjectSchema]]:
        """
        Iterates over model directories.

        This method iterates over directories within the schema directory, checking if they contain a valid model
            JSON file.
        If a valid model JSON file is found, it yields the directory path and the corresponding object schema.

        Yields:
            tuple[Path, ObjectSchema]: A tuple containing the path to the model directory and the object schema.
        """
