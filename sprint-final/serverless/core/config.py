from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Defines configuration and environment variables to be used in the project"""

    REGION_NAME: str = ""
    TABLE_NAME: str = ""
    BILLING_MODE: str = ""
    MODEL_ID: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
