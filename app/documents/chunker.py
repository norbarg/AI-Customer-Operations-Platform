import re


class TextChunker:
    def __init__(
        self,
        max_chars: int = 1200,
        overlap: int = 200,
    ) -> None:
        self.max_chars = max_chars
        self.overlap = overlap

        self.separators = [
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ]

    def split(self, text: str) -> list[str]:
        text = text.strip()

        if not text:
            return []

        chunks = self._recursive_split(
            text=text,
            separators=self.separators,
        )

        return self._add_overlap(chunks)

    def _recursive_split(
        self,
        text: str,
        separators: list[str],
    ) -> list[str]:
        if len(text) <= self.max_chars:
            return [text.strip()]

        if not separators:
            return self._hard_split(text)

        separator = separators[0]
        remaining_separators = separators[1:]

        if separator == "":
            return self._hard_split(text)

        parts = text.split(separator)

        if len(parts) == 1:
            return self._recursive_split(
                text,
                remaining_separators,
            )

        chunks: list[str] = []
        current_chunk = ""

        for part in parts:
            part = part.strip()

            if not part:
                continue

            candidate = f"{current_chunk}{separator}{part}" if current_chunk else part

            if len(candidate) <= self.max_chars:
                current_chunk = candidate
                continue

            if current_chunk:
                chunks.append(current_chunk.strip())

            if len(part) > self.max_chars:
                chunks.extend(
                    self._recursive_split(
                        part,
                        remaining_separators,
                    )
                )
                current_chunk = ""
            else:
                current_chunk = part

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def _hard_split(
        self,
        text: str,
    ) -> list[str]:
        chunks: list[str] = []

        start = 0

        while start < len(text):
            end = start + self.max_chars

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start = end

        return chunks

    def _add_overlap(
        self,
        chunks: list[str],
    ) -> list[str]:
        if not chunks or self.overlap <= 0:
            return chunks

        overlapped_chunks = [chunks[0]]

        for index in range(1, len(chunks)):
            previous_chunk = chunks[index - 1]
            current_chunk = chunks[index]

            overlap_text = self._get_overlap_text(previous_chunk)

            combined = (
                f"{overlap_text}\n\n{current_chunk}" if overlap_text else current_chunk
            )

            overlapped_chunks.append(combined.strip())

        return overlapped_chunks

    def _get_overlap_text(
        self,
        text: str,
    ) -> str:
        if len(text) <= self.overlap:
            return text.strip()

        overlap_candidate = text[-self.overlap :]

        sentence_boundaries = list(re.finditer(r"[.!?]\s+", overlap_candidate))

        if sentence_boundaries:
            first_boundary = sentence_boundaries[0]
            return overlap_candidate[first_boundary.end() :].strip()

        first_space = overlap_candidate.find(" ")

        if first_space != -1:
            return overlap_candidate[first_space + 1 :].strip()

        return overlap_candidate.strip()
