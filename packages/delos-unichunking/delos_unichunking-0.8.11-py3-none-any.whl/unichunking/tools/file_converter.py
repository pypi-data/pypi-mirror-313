"""Converts files to Office format or PDF."""

import subprocess
from pathlib import Path
from typing import Literal

from unichunking.utils import logger


def convert_file(
    input_path: Path,
    extension: Literal["docx", "xlsx", "pptx", "pdf"],
) -> Path:
    """Converts DOC/XLS/PPT and ODT/ODS/ODP to DOCX/XLSX/PPTX or PDF.

    Args:
        input_path: Path to the local file to convert.
        extension: Output format.

    Returns:
        The path to the local converted file.
    """
    try:
        subprocess.run(  # noqa: S603
            [
                Path("soffice"),
                "--headless",
                "--convert-to",
                extension,
                input_path,
                "--outdir",
                input_path.parent,
            ],
            check=True,
        )
        logger.debug(
            f"File successfully converted to {extension.upper()} format.",
        )
    except subprocess.CalledProcessError:
        logger.debug(
            "Error during conversion.",
        )

    return input_path.with_suffix(f".{extension}")
