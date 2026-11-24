from app.ai.evaluation import SemanticEvaluator

answer = (
    "Yes—provided the payment is confirmed, "
    "you have not already received a refund for that transaction, "
    "and there are no signs of fraud or account abuse, "
    "a $50 refund can be processed automatically."
)

facts = [
    "The payment must be confirmed",
    "There must be no previous refund for the same transaction",
    "There must be no signs of fraud or account abuse",
]

for fact in facts:
    match = SemanticEvaluator.find_best_match(
        fact,
        answer,
    )

    print()
    print(f"FACT: {fact}")
    print(f"SCORE: {match.score:.4f}")
    print(f"MATCH: {match.sentence}")
