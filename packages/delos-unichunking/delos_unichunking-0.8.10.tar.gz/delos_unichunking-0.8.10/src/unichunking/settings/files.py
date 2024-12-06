"""File processing settings."""

from pydantic_settings import BaseSettings


class FilesSettings(BaseSettings):
    """Accepted file types and their associated content types."""

    ACCEPTED_FILE_TYPES: list[str] = [
        "pdf",
        "docx",
        "xlsx",
        "pptx",
        "doc",
        "xls",
        "ppt",
        "odt",
        "ods",
        "odp",
        "txt",
        "csv",
        "md",
        "ipynb",
    ]

    CONTENT_TYPES: dict[str, str] = {
        "pdf": "application/pdf",
        "docx": "application/docx",
        "doc": "application/docx",
        "odt": "application/docx",
        "xlsx": "application/xlsx",
        "xls": "application/xlsx",
        "ods": "application/xlsx",
        "pptx": "application/pptx",
        "ppt": "application/pptx",
        "odp": "application/pptx",
        "txt": "text/plain",
        "csv": "text/csv",
        "md": "text/markdown",
        "ipynb": "application/x-ipynb+json",
    }
