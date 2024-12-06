from typing import TYPE_CHECKING

import amsdal_glue as glue
from amsdal_data.connections.constants import PRIMARY_PARTITION_KEY

if TYPE_CHECKING:
    from amsdal_models.classes.model import Model


def model_to_data(obj: 'Model') -> glue.Data:
    """
    Convert a model object to a data dictionary.

    Args:
        obj (Model): The model object to convert.

    Returns:
        amsdal_glue.Data: The data.
    """
    data_dump = obj.model_dump_refs(by_alias=False)
    data_dump[PRIMARY_PARTITION_KEY] = obj.object_id

    return glue.Data(data=data_dump)
