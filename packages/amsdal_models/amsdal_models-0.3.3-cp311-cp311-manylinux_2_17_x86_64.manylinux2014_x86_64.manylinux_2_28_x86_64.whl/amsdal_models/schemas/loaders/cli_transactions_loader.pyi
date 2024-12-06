from _typeshed import Incomplete
from amsdal_models.schemas.loaders.base import TransactionsLoaderBase as TransactionsLoaderBase
from collections.abc import Iterator
from pathlib import Path

class CliTransactionsLoader(TransactionsLoaderBase):
    """
    Loader for transaction files in CLI.

    This class is responsible for loading transaction files from a given application root directory. It extends the
    `TransactionsLoaderBase` to provide methods for iterating over transaction files.
    """
    _transactions_path: Incomplete
    def __init__(self, app_root: Path) -> None: ...
    def iter_transactions(self) -> Iterator[Path]:
        """
        Iterates over transaction files and yields their paths.

        This method checks if the transactions directory exists and is a directory. If the condition is met,
            it yields the paths to the transaction files in the directory.

        Yields:
            Iterator[Path]: An iterator over the paths to the transaction files in the transactions directory.
        """
    def __str__(self) -> str: ...

def _cleanup_transaction_file(source: str) -> str: ...
