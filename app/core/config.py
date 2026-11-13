from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Customer Operations Platform"
    app_version: str = "0.1.0"
    debug: bool = False

    database_url: str

    qdrant_url: str
    qdrant_collection: str

    embedding_dimensions: int = 384

    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_chat_model: str = "openrouter/free"

    rag_search_limit: int = 5
    rag_min_score: float = 0.40
    rag_max_sources: int = 5
    rag_max_context_chars: int = 6000

    hybrid_candidate_limit: int = 10
    hybrid_rrf_k: int = 60

    rerank_candidate_limit: int = 10
    rerank_min_score: float = 0.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
