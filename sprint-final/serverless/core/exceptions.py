from typing import Optional


class BaseException(Exception):
    """Base class for all custom exceptions."""

    def __init__(self, *args: object, message: Optional[str] = None) -> None:
        super().__init__(*args)
        self.message = message or "An exception occurred."


class AudioStreamNotFoundException(BaseException):
    """AudioStream was not found in Polly's response."""

    def __init__(self, *args: object, message: Optional[str] = None) -> None:
        self.message = "AudioStream was not found in Polly's response."
        super().__init__(*args, message=message or self.message)


class InstitutionAlreadyExistsException(BaseException):
    """Institution already exists."""

    def __init__(self, *args: object, message: Optional[str] = None) -> None:
        self.message = "Institution already exists."
        super().__init__(*args, message=message or self.message)


class InstitutionNotFoundException(BaseException):
    """Institution not found."""

    def __init__(self, *args: object, message: Optional[str] = None) -> None:
        self.message = "Institution not found."
        super().__init__(*args, message=message or self.message)
