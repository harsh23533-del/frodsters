from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    redis_url: str
    jwt_secret: str
    openrouter_api_key: str = ""
    elevenlabs_api_key: str = ""
    whisper_mode: str = "openai"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
