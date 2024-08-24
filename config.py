from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # database related
    db_host: str
    db_port: int
    db_name: str
    db_pwd: str
    db_usr: str

    # JWT Token Related
    secret_key: str
    refresh_secret_key: str
    algorithm: str
    token_timeout: int
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int

    db_url: str
    # internal env
    admin_api_key: str

    server: str

    class Config:
        env_file = Path(Path(__file__).resolve().parent) / ".env"


settings = Settings()
