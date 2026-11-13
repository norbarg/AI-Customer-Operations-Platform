from app.core.config import settings
from app.knowledge.search.schemas import SearchResult


class ContextBuilder:
    @staticmethod
    def build(
        results: list[SearchResult],
    ) -> tuple[str, list[SearchResult]]:
        context_parts: list[str] = []
        used_results: list[SearchResult] = []

        current_length = 0

        for index, result in enumerate(
            results[: settings.rag_max_sources],
            start=1,
        ):
            source_label = f"S{index}"

            part = (
                f"[{source_label}]\n"
                f"Document: {result.document_title}\n"
                f"Chunk: {result.chunk_index}\n\n"
                f"{result.content}"
            )

            projected_length = current_length + len(part)

            if projected_length > settings.rag_max_context_chars:
                remaining_chars = settings.rag_max_context_chars - current_length

                if remaining_chars <= 0:
                    break

                truncated_part = part[:remaining_chars]

                context_parts.append(truncated_part)
                used_results.append(result)

                break

            context_parts.append(part)
            used_results.append(result)

            current_length = projected_length

        context = "\n\n---\n\n".join(context_parts)

        return context, used_results
