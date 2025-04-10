from fastapi import APIRouter, HTTPException, status

from app.ml.parse import Mapper
from app.ml.main import ModelHandler
from app.schemas.inference import InferenceIn, InferenceOut
from app.application.contrib.exceptions import LoadError


router = APIRouter(tags=["inference"])


@router.post(
    "/inference",
    status_code=status.HTTP_200_OK,
    response_model=InferenceOut,
)
def post(data: InferenceIn) -> InferenceOut:
    parsed_data = Mapper.parse(data)

    try:
        model = ModelHandler.load_model()
        # faz a previsão com base nos dados enviados
        result = model.predict(parsed_data)

    except LoadError as exc:
        # levanta excessão se o modelo não for carregado
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc.message
        )

    # retorna o resultado pra previsão
    return {"result": int(result[0])}
