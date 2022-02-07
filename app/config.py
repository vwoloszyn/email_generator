

from pydantic import BaseSettings


class Settings(BaseSettings):
    tokenizer: str = "gpt2"
    model: str = "vwoloszyn/gtp2-email"


settings = Settings(_env_file="local.env", _env_file_encoding="utf-8")
