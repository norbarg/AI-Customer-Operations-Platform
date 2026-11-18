import asyncio
import json
from pathlib import Path

from app.ai.evaluation import SemanticEvaluator
from app.ai.judge import LLMJudge
from app.ai.rag_service import RAGService
from app.db.session import get_db
from app.knowledge.documents.chunk_repository import (
    DocumentChunkRepository,
)

EVAL_FILE = Path(__file__).resolve().parents[1] / "evals" / "rag_cases.json"

SEMANTIC_THRESHOLD = 0.45


async def evaluate() -> None:
    with EVAL_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        cases = json.load(file)

    db_generator = get_db()
    db = await anext(db_generator)

    total_cases = len(cases)

    citation_passes = 0
    no_answer_passes = 0

    total_expected_facts = 0
    matched_expected_facts = 0

    judge_correctness_scores: list[int] = []
    judge_completeness_scores: list[int] = []
    judge_groundedness_scores: list[int] = []
    judge_relevance_scores: list[int] = []

    try:
        for case in cases:
            question = case["question"]
            expected_facts = case["expected_facts"]

            response = await RAGService.answer(
                db=db,
                question=question,
            )

            print("\n" + "=" * 80)
            print(f"QUESTION: {question}")
            print(f"ANSWER:\n{response.answer}")

            if not expected_facts:
                if not response.sources:
                    no_answer_passes += 1
                    print("NO-ANSWER CHECK: PASS")
                else:
                    print("NO-ANSWER CHECK: FAIL")

                continue

            if response.sources:
                citation_passes += 1
                print("CITATIONS CHECK: PASS")
            else:
                print("CITATIONS CHECK: FAIL")

            for fact in expected_facts:
                total_expected_facts += 1

                match = SemanticEvaluator.find_best_match(
                    expected_fact=fact,
                    answer=response.answer,
                )

                matched = match.score >= SEMANTIC_THRESHOLD

                if matched:
                    matched_expected_facts += 1

                print(
                    f"{'PASS' if matched else 'FAIL'} "
                    f"| score={match.score:.4f}\n"
                    f"EXPECTED: {fact}\n"
                    f"BEST MATCH: {match.sentence}"
                )

            chunk_ids = [source.chunk_id for source in response.sources]

            chunks = await DocumentChunkRepository.get_by_ids(
                db=db,
                chunk_ids=chunk_ids,
            )

            context = "\n\n---\n\n".join(chunk.content for chunk in chunks)

            judge_result = await LLMJudge.evaluate(
                question=question,
                answer=response.answer,
                context=context,
                expected_facts=expected_facts,
            )

            judge_correctness_scores.append(judge_result.correctness)

            judge_completeness_scores.append(judge_result.completeness)

            judge_groundedness_scores.append(judge_result.groundedness)

            judge_relevance_scores.append(judge_result.relevance)

            print("\nLLM JUDGE:")
            print(f"Correctness:  {judge_result.correctness}/5")
            print(f"Completeness: {judge_result.completeness}/5")
            print(f"Groundedness: {judge_result.groundedness}/5")
            print(f"Relevance:    {judge_result.relevance}/5")

            print(f"Missing facts: {judge_result.missing_facts}")

            print(f"Unsupported claims: {judge_result.unsupported_claims}")

            print(f"Reason: {judge_result.reason}")

    finally:
        await db_generator.aclose()

    fact_recall = (
        matched_expected_facts / total_expected_facts if total_expected_facts else 0
    )

    answerable_cases = sum(1 for case in cases if case["expected_facts"])

    no_answer_cases = total_cases - answerable_cases

    citation_accuracy = citation_passes / answerable_cases if answerable_cases else 0

    no_answer_accuracy = no_answer_passes / no_answer_cases if no_answer_cases else 0

    def average(scores: list[int]) -> float:
        return sum(scores) / len(scores) if scores else 0.0

    avg_correctness = average(judge_correctness_scores)

    avg_completeness = average(judge_completeness_scores)

    avg_groundedness = average(judge_groundedness_scores)

    avg_relevance = average(judge_relevance_scores)

    print("\n" + "=" * 80)
    print("RAG ANSWER EVALUATION")
    print("=" * 80)

    print(f"Semantic fact recall: {fact_recall:.2%}")

    print(f"Citation accuracy: {citation_accuracy:.2%}")

    print(f"No-answer accuracy: {no_answer_accuracy:.2%}")

    print(f"Avg correctness:  {avg_correctness:.2f}/5")

    print(f"Avg completeness: {avg_completeness:.2f}/5")

    print(f"Avg groundedness: {avg_groundedness:.2f}/5")

    print(f"Avg relevance:    {avg_relevance:.2f}/5")


if __name__ == "__main__":
    asyncio.run(evaluate())
