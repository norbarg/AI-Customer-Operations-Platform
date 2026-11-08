class TextChunker:
    def __init__(
        self,
        max_chars: int = 1200,
        overlap: int = 200,
    ) -> None:
        self.max_chars = max_chars
        self.overlap = overlap

    def split(self, text: str) -> list[str]:
        text = text.strip()

        if not text:
            return []

        paragraphs = [
            paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()
        ]

        chunks: list[str] = []
        current_chunk = ""

        for paragraph in paragraphs:
            if len(paragraph) > self.max_chars:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""

                chunks.extend(self._split_large_text(paragraph))
                continue

            candidate = (
                f"{current_chunk}\n\n{paragraph}" if current_chunk else paragraph
            )

            if len(candidate) <= self.max_chars:
                current_chunk = candidate
                continue

            chunks.append(current_chunk)

            overlap_text = current_chunk[-self.overlap :]

            current_chunk = (
                f"{overlap_text}\n\n{paragraph}" if overlap_text else paragraph
            )

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def _split_large_text(
        self,
        text: str,
    ) -> list[str]:
        chunks: list[str] = []

        step = self.max_chars - self.overlap

        start = 0

        while start < len(text):
            end = start + self.max_chars

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start += step

        return chunks
