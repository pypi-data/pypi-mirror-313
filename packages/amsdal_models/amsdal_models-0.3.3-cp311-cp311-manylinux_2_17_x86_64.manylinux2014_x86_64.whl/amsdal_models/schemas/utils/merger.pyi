from typing import Any

def _merge_list_of_lists(parent: list[list[str]], child: list[list[str]]) -> list[list[str]]: ...
def _merge_list_fields(parent: list[Any], child: list[Any]) -> list[Any]: ...
def merge_schema(parent_schema: dict[str, Any], child_schema: dict[str, Any]) -> dict[str, Any]:
    """
    Merges the child schema into the parent schema.

    This function takes two schemas represented as dictionaries and merges the child schema into the parent schema.
    It handles merging of lists and dictionaries within the schemas, ensuring that the parent schema is updated with
    the values from the child schema.

    Args:
        parent_schema (dict[str, Any]): The parent schema to be merged into.
        child_schema (dict[str, Any]): The child schema to merge from.

    Returns:
        dict[str, Any]: The merged schema.
    """
