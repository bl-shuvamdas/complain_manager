from pydantic import BaseSettings, PostgresDsn


class Environment(BaseSettings):
    db_url: PostgresDsn
    secret_key: str

    class Config:
        env_file = ".env"


settings = Environment()
