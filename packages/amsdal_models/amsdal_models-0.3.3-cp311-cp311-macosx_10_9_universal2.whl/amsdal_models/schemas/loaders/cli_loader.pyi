from _typeshed import Incomplete
from amsdal_models.schemas.loaders.base import ConfigLoaderBase as ConfigLoaderBase, ConfigReaderMixin as ConfigReaderMixin
from amsdal_utils.models.data_models.schema import ObjectSchema as ObjectSchema
from collections.abc import Iterator
from pathlib import Path

MODEL_JSON_FILE: str

class CliConfigLoader(ConfigReaderMixin, ConfigLoaderBase):
    """
    Loader for configuration files in CLI.

    This class is responsible for loading configuration files from a given configuration directory. It extends the
    `ConfigReaderMixin` and `ConfigLoaderBase` to provide methods for iterating over configuration files and directories
    """
    _config_dir: Incomplete
    def __init__(self, config_dir: Path) -> None: ...
    def __str__(self) -> str: ...
    def iter_configs(self) -> Iterator[ObjectSchema]:
        """
        Iterates over configuration files and yields their schemas.

        This method iterates over JSON files in the configuration directory. For each JSON file,
            it checks if the file is a schema file.
            If it is, it reads the configurations from the file and yields the schemas.

        Yields:
            Iterator[ObjectSchema]: An iterator over the schemas of the configuration files.
        """
    def iter_json_files(self) -> Iterator[Path]:
        """
        Iterates over JSON files in the configuration directory and yields their paths.

        This method checks if the configuration directory exists. For each item in the directory,
            it checks if the item is a directory and contains a model JSON file. If both conditions are met,
            it yields the path to the model JSON file.

        Yields:
            Iterator[Path]: An iterator over the paths to the JSON files in the configuration directory.
        """
