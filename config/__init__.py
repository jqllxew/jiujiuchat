import os

from pydantic_settings import BaseSettings


class Configs(BaseSettings):
    VERSION: str = "0.1.0"  # Project version
    API_BASE_URL: str = "/api"  # API version string
    PROJECT_NAME: str = "lobe-chat-plugin"
    PORT: int = 7667
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
                f"mysql+mysqlconnector://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
                f"@{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
            )
        return self.DB_URL
