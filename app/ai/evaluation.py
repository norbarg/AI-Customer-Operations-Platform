import re
from dataclasses import dataclass

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


@dataclass
class SemanticMatch:
    score: float
    sentence: str


class SemanticEvaluator:
    _model = SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2")

    @classmethod
    def find_best_match(
        cls,
        expected_fact: str,
        answer: str,
    ) -> SemanticMatch:
        sentences = cls._split_sentences(answer)

        if not sentences:
            return SemanticMatch(
                score=0.0,
                sentence="",
            )

        fact_embedding = cls._model.encode(
            expected_fact,
            normalize_embeddings=True,
        )

        sentence_embeddings = cls._model.encode(
            sentences,
            normalize_embeddings=True,
        )

        similarities = cos_sim(
            fact_embedding,
            sentence_embeddings,
        )[0]

        best_index = int(similarities.argmax().item())

        return SemanticMatch(
            score=float(similarities[best_index].item()),
            sentence=sentences[best_index],
        )

    @staticmethod
    def _split_sentences(
        text: str,
    ) -> list[str]:
        sentences = re.split(
            r"(?<=[.!?])\s+|\n+",
            text.strip(),
        )

        return [sentence.strip() for sentence in sentences if sentence.strip()]
