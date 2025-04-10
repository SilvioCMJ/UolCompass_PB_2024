import logging
import boto3
from io import BytesIO

from sklearn.ensemble import RandomForestClassifier
from app.application.core.config import settings
from app.ml.main import MLModelHandler

logger = logging.getLogger(__name__)


class MLModelHandler(MLModelHandler):
    def s3_client(self) -> BytesIO:
        return boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN,
            region_name=settings.AWS_REGION_NAME,
        ).client("s3")


    def get_model(self):
        return super().get_model()


    def load_model(self) -> RandomForestClassifier:
        return super().load_model()


ModelHandler = MLModelHandler()