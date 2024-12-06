"""Page computing."""

import re
from pathlib import Path
from typing import Any

import pymupdf

from unichunking.settings import unisettings
from unichunking.tools import convert_file
from unichunking.types import Chunk, StatusManager
from unichunking.utils import logger


def _strip_text(txt: str) -> str:
    image_description_pattern = r"@_@_@ IMAGE \d+ @_@_@"
    return (
        re.sub(image_description_pattern, "", txt)
        .replace("** Table : ", "")
        .replace(" ; End Of Table **", "")
        .replace("** Chart : ", "")
        .replace(" ; End Of Chart **", "")
        .replace(" ", "")
        .replace("\n", "")
        .replace("\xa0", "")
        .replace("-", "")
        .lower()
    )


def _intersection_of_length_n(
    chunk: str,
    block: str,
    intersection_length: int,
) -> bool:
    for start in range(len(block) - intersection_length + 1):
        if block[start : start + intersection_length] in chunk:
            return True
    return False


def _longest_intersection(
    chunk: str,
    block: str,
    min_intersection_length: int,
) -> int:
    floor = min_intersection_length
    ceiling = min(len(block), len(chunk))
    intersection_length = min_intersection_length
    while floor < ceiling:
        intersection_length = (floor + ceiling + 1) // 2
        if _intersection_of_length_n(
            chunk=chunk,
            block=block,
            intersection_length=intersection_length,
        ):
            floor = intersection_length
        else:
            ceiling = intersection_length - 1
    return (
        floor
        if _intersection_of_length_n(
            chunk=chunk,
            block=block,
            intersection_length=floor,
        )
        else 0
    )


def _positions_intersect(
    position1: dict[str, float],
    position2: dict[str, float],
) -> bool:
    return (
        (
            position1["x0"] <= position2["x0"] <= position1["x1"]
            and position1["y0"] <= position2["y0"] <= position1["y1"]
        )
        or (
            position1["x0"] <= position2["x1"] <= position1["x1"]
            and position1["y0"] <= position2["y0"] <= position1["y1"]
        )
        or (
            position1["x0"] <= position2["x0"] <= position1["x1"]
            and position1["y0"] <= position2["y1"] <= position1["y1"]
        )
        or (
            position1["x0"] <= position2["x1"] <= position1["x1"]
            and position1["y0"] <= position2["y1"] <= position1["y1"]
        )
    )


def _edit_chunk_positions(
    chunk: Chunk,
) -> None:
    different_positions: list[dict[str, float]] = []
    for position in chunk.metadata["positions"]:
        position["x0"] = max(0, position["x0"])
        position["y0"] = max(0, position["y0"])
        position["x1"] = min(1, position["x1"])
        position["y1"] = min(1, position["y1"])
        new = True
        for different_position in different_positions:
            if _positions_intersect(
                position,
                different_position,
            ) or _positions_intersect(different_position, position):
                different_position["x0"] = min(
                    different_position["x0"],
                    position["x0"],
                )
                different_position["y0"] = min(
                    different_position["y0"],
                    position["y0"],
                )
                different_position["x1"] = max(
                    different_position["x1"],
                    position["x1"],
                )
                different_position["y1"] = max(
                    different_position["y1"],
                    position["y1"],
                )
                new = False
                break
        if new:
            different_positions.append(position)
    chunk.metadata["positions"] = different_positions


def edit_positions_on_page(
    chunks_pages: list[list[Chunk]],
    extension: str,
) -> list[list[Chunk]]:
    """Adjusts the positions of subelements in Chunk objects to avoid overlaps.

    For DOCX : no highlighting because sourcing is not precise enough.

    Args:
        chunks_pages: A list of lists where chunks_pages[i][j] is Chunk j on page i.
        extension: File extension.

    Returns:
        The same list of lists of Chunk objects, whoses positions where adjusted.
    """
    if extension == "docx":
        for page in chunks_pages:
            for chunk in page:
                chunk.metadata["positions"] = [{"x0": 0, "y0": 0, "x1": 0, "y1": 0}]

    else:
        for page in chunks_pages:
            for chunk in page:
                _edit_chunk_positions(chunk)

    return chunks_pages


def _find_possible_pages(
    cur_page: int,
    pages_reach: int,
    pages: list[list[str]],
) -> list[int]:
    possible_pages: list[int] = [cur_page]
    for _ in range(pages_reach):
        for page_idx in range(possible_pages[-1] + 1, len(pages)):
            if any(block for block in pages[page_idx]):
                possible_pages.append(page_idx)
                return possible_pages
    return possible_pages


async def compute_pages(
    path: Path,
    chunks: list[Chunk],
    num_pages: int,
    status_manager: Any = None,
    increment_reach: bool = True,
) -> tuple[list[Chunk], int]:
    """Corrects the pagination of DOCX chunks by comparing the text to the converted PDF.

    Args:
        path: Path to the local file.
        chunks: List of Chunk objects.
        num_pages: Number of pages originally found through Page Breaks.
        status_manager: Optional, special object to manage task progress.
        increment_reach: Boolean value (True by default) indicating whether or not to increase the page reach when accumulating chunks on the same page.

    Returns:
        A tuple containing an int and a list:
        - The actual number of pages in the document.
        - A list containing the Chunk objects, updated with the correct page numbers.
    """
    if not status_manager:
        status_manager = StatusManager(task="Page computing")

    remove_local_file = False
    if not path.with_suffix(".pdf").exists():
        logger.debug("Converting DOCX-like file to PDF format...")
        convert_file(path, "pdf")
        remove_local_file = True
        logger.debug("PDF conversion done.")

    min_intersection_length = unisettings.chunking.MIN_INTERSECTION_LENGTH

    with pymupdf.Document(path.with_suffix(".pdf")) as doc:
        if num_pages == doc.page_count:  # type: ignore
            return chunks, num_pages

        logger.debug(
            f"Pdf.page_count ({doc.page_count}) does not match num_pages ({num_pages}).",  # type: ignore
        )
        logger.debug(
            f"Computing page numbers with minimal intersection length {min_intersection_length}...",
        )

        pages = [
            [_strip_text(block[4]) for block in page.get_text("blocks")]  # type: ignore
            for page in doc.pages()  # type: ignore
        ]

    best_page = 0
    pages_reach = 1

    for chunk_idx in range(len(chunks)):
        if chunk_idx % int(len(chunks) / 30 + 1) == 0:
            page_progress = int((chunk_idx + 1) / len(chunks) * 100)
            await status_manager.update_status(
                progress=page_progress,
                start=status_manager.start,
                end=status_manager.end,
            )

        chunk = chunks[chunk_idx]
        stripped_chunk = _strip_text(chunk.content)

        cur_page = min(max(best_page, chunk.metadata["page"] - 1), len(pages) - 1)

        best_intersection = sum(
            _longest_intersection(
                chunk=stripped_chunk,
                block=block,
                min_intersection_length=min_intersection_length,
            )
            for block in pages[cur_page]
        )
        best_page = cur_page

        possible_pages = _find_possible_pages(
            cur_page=cur_page,
            pages_reach=pages_reach,
            pages=pages,
        )

        for page_idx in possible_pages[1:]:
            page_intersection = sum(
                _longest_intersection(
                    chunk=stripped_chunk,
                    block=block,
                    min_intersection_length=min_intersection_length,
                )
                for block in pages[page_idx]
            )
            if page_intersection > best_intersection:
                best_intersection = page_intersection
                best_page = page_idx

        chunk.metadata["page"] = best_page + 1
        if increment_reach:
            pages_reach += 1 if best_page == cur_page else 0

    if remove_local_file:
        path.with_suffix(".pdf").unlink()
        logger.debug("Deleted local PDF file.")
    return chunks, len(pages)
