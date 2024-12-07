import amsdal_glue as glue
from amsdal_models.classes.model import Model as Model

def model_to_data(obj: Model) -> glue.Data:
    """
    Convert a model object to a data dictionary.

    Args:
        obj (Model): The model object to convert.

    Returns:
        amsdal_glue.Data: The data.
    """
