from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    POSTGRES_DB: str

    SECRET_API_KEY: str

    ACCESS_TOKEN_MINUTES: int
    REFRESH_TOKEN_DAYS: int

    API_ACCESS_TOKEN_MINUTES: int
    API_REFRESH_TOKEN_DAYS: int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def DATABASE_URL(self) -> str:
        """:return: URL для рабочей БД"""
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}"
            f"/{self.POSTGRES_DB}"
        )

    @property
    def ALEMBIC_DATABASE_URL(self):
        """:return: URL для работы с миграциями в рабочей БД"""
        return (
            f"postgresql://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}"
            f"/{self.POSTGRES_DB}"
        )


settings = Settings()
