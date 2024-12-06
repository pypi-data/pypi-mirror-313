from _typeshed import Incomplete
from amsdal_models.schemas.loaders.base import StaticsLoaderBase as StaticsLoaderBase
from collections.abc import Iterator
from pathlib import Path

class CliStaticsLoader(StaticsLoaderBase):
    """
    Loader for static files in CLI.

    This class is responsible for loading static files from a given application root directory. It extends the
    `StaticsLoaderBase` to provide methods for iterating over static files.
    """
    _app_root: Incomplete
    def __init__(self, app_root: Path) -> None: ...
    def iter_static(self) -> Iterator[Path]:
        """
        Iterates over static files and yields their paths.

        This method checks if the static directory exists and is a directory. For each item in the directory,
            it checks if the item is a file. If the condition is met, it yields the path to the static file.

        Yields:
            Iterator[Path]: An iterator over the paths to the static files in the static directory.
        """
    def __str__(self) -> str: ...
