from sentence_transformers import SentenceTransformer


class EmbeddingService:
    _model = SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2")

    @classmethod
    async def embed_text(
        cls,
        text: str,
    ) -> list[float]:
        embedding = cls._model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    @classmethod
    async def embed_texts(
        cls,
        texts: list[str],
    ) -> list[list[float]]:
        embeddings = cls._model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()
