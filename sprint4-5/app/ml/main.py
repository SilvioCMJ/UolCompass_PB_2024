import logging
import boto3
import joblib
from io import BytesIO

from sklearn.ensemble import RandomForestClassifier
from app.application.contrib.exceptions import LoadError
from app.application.core.config import settings
from app.ml.base import MLModelHandlerInterface

logger = logging.getLogger(__name__)


class MLModelHandler(MLModelHandlerInterface[RandomForestClassifier]):
    def s3_client(self):
        return boto3.client("s3")


    def get_model(self) -> BytesIO:
        response = self.s3_client().get_object(
            Bucket=settings.S3_BUCKET, Key=settings.S3_MODEL_PATH
        )
        return BytesIO(response["Body"].read())


    def load_model(self) -> RandomForestClassifier:
        error_message = "Erro ao carregar o modelo do S3."
        try:
            model = joblib.load(self.get_model())
        except Exception as exc:
            logger.info(f"{error_message}: {exc}")
            raise LoadError(message=error_message)

        return model


ModelHandler = MLModelHandler()