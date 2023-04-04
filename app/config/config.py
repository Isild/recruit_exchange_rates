from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Exchange Rates"
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 5

    class Config:
        env_file = ".env"
