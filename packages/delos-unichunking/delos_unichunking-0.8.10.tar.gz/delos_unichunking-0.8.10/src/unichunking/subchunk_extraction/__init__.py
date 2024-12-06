"""Subchunks extraction for all the supported types."""

from .docx_sub_chunking import extract_subchunks_docx
from .ipynb_sub_chunking import extract_subchunks_ipynb
from .pdf_sub_chunking import extract_subchunks_pdf
from .pptx_sub_chunking import extract_subchunks_pptx
from .txt_sub_chunking import extract_subchunks_txt
from .xlsx_sub_chunking import extract_subchunks_xlsx

__all__ = [
    "extract_subchunks_docx",
    "extract_subchunks_ipynb",
    "extract_subchunks_pdf",
    "extract_subchunks_pptx",
    "extract_subchunks_txt",
    "extract_subchunks_xlsx",
]
