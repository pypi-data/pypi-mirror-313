from amsdal_utils.errors import AmsdalError


class AmsdalValidationError(AmsdalError):
    def __init__(self, message: str) -> None:
        self.message = message
