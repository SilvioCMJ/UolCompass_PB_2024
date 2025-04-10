from pydantic_settings import BaseSettings, SettingsConfigDict


# Define configurações e variveis de ambiente que serão usadas no projeto
class Settings(BaseSettings):
    PROJECT_NAME: str = "Inference Service"
    ROOT_PATH: str = "/api/v1"

    S3_BUCKET: str = ""
    S3_MODEL_PATH: str = ""

    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_SESSION_TOKEN: str = ""
    AWS_REGION_NAME: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
