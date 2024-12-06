from _typeshed import Incomplete
from amsdal_models.schemas.loaders.base import FixturesLoaderBase as FixturesLoaderBase
from collections.abc import Iterator
from pathlib import Path

FIXTURES: str
logger: Incomplete
FIXTURES_JSON_FILE: str
MODEL_JSON_FILE: str

class CliFixturesLoader(FixturesLoaderBase):
    """
    Loader for fixtures in CLI.

    This class is responsible for loading fixtures from a given schema directory. It extends the `FixturesLoaderBase`
    to provide methods for iterating over fixture files and directories.
    """
    models_with_fixtures: Incomplete
    def __init__(self, schema_dir: Path) -> None: ...
    def iter_fixtures(self) -> Iterator[Path]:
        """
        Iterates over fixture files and yields their paths.

        This method creates a temporary directory and writes fixture data to a JSON file within that directory.
            It collects fixture data from CSV and JSON files in the model directories and writes them to the JSON file.
            The path to the JSON file is then yielded.

        Yields:
            Iterator[Path]: An iterator over the paths to the JSON files containing the fixture data.
        """
    def iter_fixture_files(self) -> Iterator[Path]:
        """
        Iterates over fixture files and yields their paths.

        This method creates a temporary directory and copies fixture files from the model directories to this temporary
        directory. It then yields the path to the temporary directory containing the copied fixture files.

        Yields:
            Iterator[Path]: An iterator over the paths to the temporary directories containing the copied fixture files.
        """
    def __str__(self) -> str: ...
