from fastapi import FastAPI
from app.application.core.config import settings
from app.application.core.logging import setup_logging
from app.presentation.views.inference import router as inference_router


# aplicação
class App(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            title=settings.PROJECT_NAME,
            version="1.0",
            root_path=settings.ROOT_PATH
        )
        setup_logging()
        self._include_routers()

    def _include_routers(self) -> None:
        """
        Recebe `n` chamadas de `FastAPI.include_router`
        no corpo para incluir rotas na aplicação.\n
        Deve ser usado apenas dentro da aplicação.

        **Utilização**:\n
            from fastapi import FastAPI

            class App(FastAPI):
                ...
                self._include_routers()
                ...
        """

        self.include_router(inference_router)


app = App()
