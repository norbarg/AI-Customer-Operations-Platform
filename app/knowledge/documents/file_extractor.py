from io import BytesIO
from pathlib import Path
from typing import ClassVar

from docx import Document as DocxDocument
from pypdf import PdfReader


class UnsupportedFileTypeError(Exception):
    pass


class FileTextExtractor:
    SUPPORTED_EXTENSIONS: ClassVar[set[str]] = {
        ".txt",
        ".md",
        ".pdf",
        ".docx",
    }

    @classmethod
    def extract(
        cls,
        filename: str,
        content: bytes,
    ) -> str:
        extension = Path(filename).suffix.lower()

        if extension not in cls.SUPPORTED_EXTENSIONS:
            raise UnsupportedFileTypeError(f"Unsupported file type: {extension}")

        if extension in {".txt", ".md"}:
            text = cls._extract_text(content)

        elif extension == ".pdf":
            text = cls._extract_pdf(content)

        elif extension == ".docx":
            text = cls._extract_docx(content)

        else:
            raise UnsupportedFileTypeError(f"Unsupported file type: {extension}")

        text = text.strip()

        if not text:
            raise ValueError("No text could be extracted from the file")

        return text

    @staticmethod
    def _extract_text(
        content: bytes,
    ) -> str:
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Text file must use UTF-8 encoding") from exc

    @staticmethod
    def _extract_pdf(
        content: bytes,
    ) -> str:
        reader = PdfReader(BytesIO(content))

        pages = [page.extract_text() or "" for page in reader.pages]

        return "\n\n".join(pages)

    @staticmethod
    def _extract_docx(
        content: bytes,
    ) -> str:
        document = DocxDocument(BytesIO(content))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n\n".join(paragraphs)
