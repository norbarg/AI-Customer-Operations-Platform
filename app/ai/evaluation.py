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
        fragments = cls._split_fragments(answer)

        if not fragments:
            return SemanticMatch(
                score=0.0,
                sentence="",
            )

        fact_embedding = cls._model.encode(
            expected_fact,
            normalize_embeddings=True,
        )

        fragment_embeddings = cls._model.encode(
            fragments,
            normalize_embeddings=True,
        )

        similarities = cos_sim(
            fact_embedding,
            fragment_embeddings,
        )[0]

        best_index = int(similarities.argmax().item())

        return SemanticMatch(
            score=float(similarities[best_index].item()),
            sentence=fragments[best_index],
        )

    @staticmethod
    def _split_fragments(
        text: str,
    ) -> list[str]:
        sentences = re.split(
            r"(?<=[.!?])\s+|\n+",
            text.strip(),
        )

        fragments: list[str] = []

        for sentence in sentences:
            sentence = sentence.strip()

            if not sentence:
                continue

            fragments.append(sentence)

            clauses = re.split(
                r"\s*(?:,|;|\band\b|\bbut\b)\s*",
                sentence,
                flags=re.IGNORECASE,
            )

            for clause in clauses:
                clause = clause.strip(" -*•\t")

                if clause and clause != sentence and len(clause) >= 10:
                    fragments.append(clause)

        return list(dict.fromkeys(fragments))
