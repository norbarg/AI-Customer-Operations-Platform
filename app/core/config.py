from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Customer Operations Platform"
    app_version: str = "0.1.0"
    debug: bool = False

    database_url: str

    qdrant_url: str
    qdrant_collection: str

    # openai_api_key: str
    # openai_embedding_model: str = "text-embedding-3-small"
    # openai_embedding_dimensions: int = 1536

    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    embedding_model: str
    embedding_dimensions: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
