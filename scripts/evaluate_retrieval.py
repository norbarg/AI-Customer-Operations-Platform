import asyncio
import json
from pathlib import Path

from app.ai.reranker import RerankerService
from app.core.config import settings
from app.db.session import get_db
from app.knowledge.search.service import SearchService

EVAL_FILE = Path(__file__).resolve().parents[1] / "evals" / "retrieval_cases.json"


async def evaluate() -> None:
    with EVAL_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        cases = json.load(file)

    db_generator = get_db()
    db = await anext(db_generator)

    total_answerable = 0
    hits = 0
    reciprocal_rank_sum = 0.0

    total_unanswerable = 0
    correct_rejections = 0

    try:
        for case in cases:
            question = case["question"]

            expected_documents = case["expected_documents"]

            candidates = await SearchService.search(
                db=db,
                query=question,
                limit=settings.rerank_candidate_limit,
                score_threshold=settings.rag_min_score,
            )

            results = RerankerService.rerank(
                query=question,
                results=candidates,
                limit=settings.rag_search_limit,
            )

            print("\n" + "=" * 80)
            print(f"QUESTION: {question}")
            print(f"EXPECTED: {expected_documents}")

            if results:
                for rank, result in enumerate(
                    results,
                    start=1,
                ):
                    print(
                        f"{rank}. "
                        f"{result.document_title} "
                        f"| chunk={result.chunk_index} "
                        f"| score={result.score:.4f}"
                    )
            else:
                print("RESULTS: no relevant chunks")

            # No-answer case:
            # expected_documents = []
            if not expected_documents:
                total_unanswerable += 1

                if not results:
                    correct_rejections += 1
                    print("RESULT: PASS")
                else:
                    print("RESULT: FAIL")

                continue

            total_answerable += 1

            matching_rank = next(
                (
                    rank
                    for rank, result in enumerate(
                        results,
                        start=1,
                    )
                    if result.document_title in expected_documents
                ),
                None,
            )

            if matching_rank is None:
                print("RESULT: FAIL")
                continue

            hits += 1

            reciprocal_rank_sum += 1 / matching_rank

            print(f"RESULT: PASS (rank={matching_rank})")

    finally:
        await db_generator.aclose()

    hit_rate = hits / total_answerable if total_answerable else 0

    mrr = reciprocal_rank_sum / total_answerable if total_answerable else 0

    rejection_accuracy = (
        correct_rejections / total_unanswerable if total_unanswerable else 0
    )

    print("\n" + "=" * 80)
    print("RETRIEVAL EVALUATION")
    print("=" * 80)

    print(f"Hit@{settings.rag_search_limit}: {hit_rate:.2%}")

    print(f"MRR: {mrr:.4f}")

    print(f"No-answer accuracy: {rejection_accuracy:.2%}")


if __name__ == "__main__":
    asyncio.run(evaluate())
