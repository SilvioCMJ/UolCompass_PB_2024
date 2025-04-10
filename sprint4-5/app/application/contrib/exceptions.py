from typing import Optional


class BaseException(Exception):
    """Base para excessões customizadas."""

    def __init__(self, *args: object, message: Optional[str] = None) -> None:
        super().__init__(*args)

        if message:
            self.message = message


class LoadError(BaseException):
    """Ocorreu um erro ao carregar o arquivo."""

    def __init__(
        self,
        *args: object,
        message: Optional[str] = None,
    ) -> None:
        self.message = "Erro ao carregar o arquivo."
        super().__init__(*args, message=message)
