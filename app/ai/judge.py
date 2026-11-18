import json

from pydantic import BaseModel, Field

from app.ai.client import openrouter_client
from app.core.config import settings


class JudgeResult(BaseModel):
    correctness: int = Field(ge=1, le=5)
    completeness: int = Field(ge=1, le=5)
    groundedness: int = Field(ge=1, le=5)
    relevance: int = Field(ge=1, le=5)

    missing_facts: list[str]
    unsupported_claims: list[str]

    reason: str


class LLMJudge:
    @staticmethod
    async def evaluate(
        question: str,
        answer: str,
        context: str,
        expected_facts: list[str],
    ) -> JudgeResult:
        expected_facts_text = "\n".join(f"- {fact}" for fact in expected_facts)

        response = await openrouter_client.chat.completions.create(
            model=settings.openrouter_judge_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are evaluating the quality of a RAG system.\n"
                        "Be strict and objective.\n\n"
                        "Score each criterion from 1 to 5:\n"
                        "1. correctness: factual correctness of the answer.\n"
                        "2. completeness: whether important expected facts "
                        "needed to answer the question are covered.\n"
                        "3. groundedness: whether company-specific claims "
                        "are supported by the provided context.\n"
                        "4. relevance: whether the answer directly answers "
                        "the user's question without unnecessary content.\n\n"
                        "Do not penalize harmless paraphrasing.\n"
                        "Do not require every expected fact if it is not "
                        "necessary to answer the question.\n"
                        "A claim is unsupported only if it is not justified "
                        "by the provided context.\n\n"
                        "Return ONLY valid JSON."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"QUESTION:\n{question}\n\n"
                        f"EXPECTED FACTS:\n{expected_facts_text}\n\n"
                        f"RETRIEVED CONTEXT:\n{context}\n\n"
                        f"GENERATED ANSWER:\n{answer}\n\n"
                        "Return this JSON structure:\n"
                        "{\n"
                        '  "correctness": 1,\n'
                        '  "completeness": 1,\n'
                        '  "groundedness": 1,\n'
                        '  "relevance": 1,\n'
                        '  "missing_facts": [],\n'
                        '  "unsupported_claims": [],\n'
                        '  "reason": ""\n'
                        "}"
                    ),
                },
            ],
            temperature=0,
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError("Judge returned an empty response")

        json_content = LLMJudge._extract_json(content)

        data = json.loads(json_content)

        return JudgeResult.model_validate(data)

    @staticmethod
    def _extract_json(
        content: str,
    ) -> str:
        content = content.strip()

        start = content.find("{")
        end = content.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("Judge response does not contain JSON")

        return content[start : end + 1]
