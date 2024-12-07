from _typeshed import Incomplete
from amsdal_models.schemas.data_models.options import OptionSchema as OptionSchema
from amsdal_models.schemas.loaders.base import OptionsLoaderBase as OptionsLoaderBase
from amsdal_models.schemas.loaders.utils import load_object_schema_from_json_file as load_object_schema_from_json_file
from collections.abc import Iterator
from pathlib import Path

logger: Incomplete

class CliOptionsLoader(OptionsLoaderBase):
    """
    Loader for options configuration files in CLI.

    This class is responsible for loading options configuration files from a given configuration directory. It extends
        the `OptionsLoaderBase` to provide methods for iterating over options files and directories.
    """
    _app_root: Incomplete
    def __init__(self, config_dir: Path) -> None: ...
    def __str__(self) -> str: ...
    def iter_options(self) -> Iterator[OptionSchema]:
        """
        Iterates over options configuration files and yields their schemas.

        This method iterates over JSON files in the options directory. For each JSON file, it reads the options from
            the file and yields the schemas.

        Yields:
            Iterator[OptionSchema]: An iterator over the schemas of the options configuration files.
        """
    def iter_json_files(self) -> Iterator[Path]:
        """
        Iterates over JSON files in the options directory and yields their paths.

        This method checks if the options directory exists and is a directory. For each item in the directory,
            it checks if the item is a file and has a `.json` extension. If both conditions are met,
            it yields the path to the JSON file.

        Yields:
            Iterator[Path]: An iterator over the paths to the JSON files in the options directory.
        """
    @staticmethod
    def read_options_from_file(json_file: Path) -> Iterator[OptionSchema]:
        """
        Reads options from a JSON file and yields their schemas.

        This method reads the options from the given JSON file and yields the schemas of the options.

        Args:
            json_file (Path): The path to the JSON file containing the options.

        Yields:
            Iterator[OptionSchema]: An iterator over the schemas of the options in the JSON file.
        """
