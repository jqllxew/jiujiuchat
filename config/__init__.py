import os

from pydantic_settings import BaseSettings


class Configs(BaseSettings):
    VERSION: str = "0.1.0"  # Project version
    API_BASE_URL: str = "/api"  # API version string
    PROJECT_NAME: str = "lobe-chat-plugin"
    PORT: int = 7667
    DOMAIN: str = os.getenv("DOMAIN", "127.0.0.1:7667")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "jqllxew")
    # ocr
    VOLC_ACCESS_KEY: str = os.getenv("VOLC_ACCESS_KEY", "")
    VOLC_SECRET_KEY: str = os.getenv("VOLC_SECRET_KEY", "")
    # 对象存储
    OSS_ACCESS_KEY_ID: str = os.getenv("OSS_ACCESS_KEY_ID", "")
    OSS_ACCESS_KEY_SECRET: str = os.getenv("OSS_ACCESS_KEY_SECRET", "")
    OSS_REGION: str = os.getenv("OSS_REGION", "")
    OSS_BUCKET: str = os.getenv("OSS_BUCKET", "")
    OSS_ENDPOINT: str = os.getenv("OSS_ENDPOINT", "")
    # 企微
    QW_TOKEN: str = os.getenv("QW_TOKEN", "")
    QW_ENCODING_AES_KEY: str = os.getenv("QW_ENCODING_AES_KEY", "")
    QW_CORP_ID: str = os.getenv("QW_CORP_ID", "")
    QW_CORP_SECRET: str = os.getenv("QW_CORP_SECRET", "")
    # database
    DB_URL: str = ""
    DB_SERVER: str = os.getenv("MYSQL_SERVER", "localhost")
    DB_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
    DB_USER: str = os.getenv("MYSQL_USER", "jqllxew")
    DB_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "jqllxew")
    DB_DATABASE: str = os.getenv("MYSQL_DATABASE", "test")

    @property
    def get_db_url(self) -> str:
        if not self.DB_URL:
            self.DB_URL = (
                f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_SERVER}:{self.DB_PORT}/{self.DB_DATABASE}"
            )
        return self.DB_URL

    class Config:
        env_file = ".env"


configs = Configs()
