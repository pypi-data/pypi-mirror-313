"""Chhunk formating."""

import copy
from pathlib import Path
from typing import Any, Callable, Literal
from uuid import uuid4

from llmax import tokens

from unichunking.settings import unisettings
from unichunking.tools import clean_chunk
from unichunking.types import Chunk, StatusManager, SubChunk

from .pages import compute_pages, edit_positions_on_page
from .subchunking import extract_subchunks
from .utils import compute_bbox

Action = Literal["describe", "transcribe"]


def split_chunks_with_overlap(
    chunks: list[SubChunk],
    page_id: int,
    file_name: str,
    file_hash: str = "",
    k_min: int = unisettings.chunking.DEFAULT_K_MIN,
    k_max: int = unisettings.chunking.DEFAULT_K_MIN
    + unisettings.chunking.DEFAULT_MIN_MAX_GAP,
    overlap: int = unisettings.chunking.DEFAULT_OVERLAP,
) -> list[Chunk]:
    """Splits the text allowing some overlapping.

    - chunks: les différents chunks extraits du document
    - k_min: nombre de tokens minimal par chunk
    - k_max: nombre maximal de tokens par chunk
    - overlap: nombre de caractères pour l'overlap.
    """
    if not (0 < k_min <= k_max) or overlap < 0:
        message = "Please ensure that 0 < K_MIN <= K_MAX and that overlap >= 0"
        raise ValueError(message)

    chunks_final: list[Chunk] = []

    current_chunk = ""
    current_positions = []

    for it, chunk in enumerate(chunks):
        if tokens.count(current_chunk) + tokens.count(
            chunk.content,
        ) < k_max or it + 1 == len(chunks):
            current_chunk += f" {chunk.content}"
            current_positions.append(chunk.position.to_dict())
            if tokens.count(current_chunk) >= k_min or (it + 1 == len(chunks)):
                curr_chunk = Chunk(
                    chunk_num=len(chunks_final) + 1,
                    content=current_chunk,
                    metadata={
                        "page": page_id,
                        "file_name": file_name,
                        "positions": copy.deepcopy(current_positions),
                    },
                    embedding=[0] * 1536,
                    chunk_uid=uuid4(),
                    file_hash=file_hash,
                    num_tokens=tokens.count(current_chunk),
                )
                curr_chunk.metadata["bbox"] = compute_bbox([curr_chunk])
                curr_chunk = clean_chunk(curr_chunk)
                if curr_chunk.content:
                    chunks_final.append(curr_chunk)
                current_positions = [chunk.position.to_dict()]
                current_chunk = current_chunk[-overlap:] if overlap else ""

        else:
            curr_chunk = Chunk(
                chunk_num=len(chunks_final) + 1,
                content=current_chunk,
                metadata={
                    "page": page_id,
                    "file_name": file_name,
                    "positions": copy.deepcopy(current_positions),
                },
                embedding=[0] * 1536,
                chunk_uid=uuid4(),
                file_hash=file_hash,
                num_tokens=tokens.count(current_chunk),
            )
            curr_chunk.metadata["bbox"] = compute_bbox([curr_chunk])
            curr_chunk = clean_chunk(curr_chunk)
            if curr_chunk.content:
                chunks_final.append(curr_chunk)
            current_positions = [chunk.position.to_dict()]
            current_chunk = (
                current_chunk[-overlap:] + chunk.content if overlap else chunk.content
            )

    return chunks_final


def default_function(base64_image: str) -> str:  # noqa: ARG001
    """Default function."""
    return ""


async def build_chunked_pages(
    path: Path,
    file_hash: str = "",
    k_min: int = unisettings.chunking.DEFAULT_K_MIN,
    overlap: int = unisettings.chunking.DEFAULT_OVERLAP,
    status_manager: Any = None,
    function: Callable[[str], str] = default_function,
) -> tuple[list[list[Chunk]], int]:
    """Returns a list of Pages and Chunks objects, once extracted, merged when necessary, cleaned and embedded."""
    k_max = k_min + unisettings.chunking.DEFAULT_MIN_MAX_GAP

    extension = path.suffix[1:]
    if unisettings.files.CONTENT_TYPES[extension] == "application/docx":
        extension = "docx"

    chunks: list[Chunk] = []
    chunks_pages: list[list[Chunk]] = []
    file_name = path.name

    if not status_manager:
        status_manager = StatusManager(task="Subchunk extraction")
    status_manager.start = 0
    status_manager.end = 40

    chunks_extracted = await extract_subchunks(
        path,
        k_max=k_max,
        status_manager=status_manager,
        function=function,
    )

    pages_numbers = [ch.page for ch in chunks_extracted]
    if len(pages_numbers) == 0:
        return [[]], 0

    num_pages = max(pages_numbers) + 1
    status_manager.task = "Chunk formating"
    status_manager.start = 40
    status_manager.end = 75 if extension == "docx" else 100
    for page_id in range(num_pages):
        if page_id % int(num_pages / 30 + 1) == 0:
            page_progress = int((page_id + 1) / num_pages * 100)
            await status_manager.update_status(
                progress=page_progress,
                start=status_manager.start,
                end=status_manager.end,
            )

        relevant_chunks = [ch for ch in chunks_extracted if ch.page == page_id]
        res = split_chunks_with_overlap(
            relevant_chunks,
            file_hash=file_hash,
            file_name=file_name,
            page_id=page_id + 1,
            k_min=k_min,
            k_max=k_max,
            overlap=overlap,
        )
        chunks.extend(res)
        chunks_pages.append(res)

    if extension == "docx":
        status_manager.task = "Page computing"
        status_manager.start = 75
        status_manager.end = 100

        chunks, num_pages = await compute_pages(
            path=path,
            chunks=chunks,
            num_pages=num_pages,
            status_manager=status_manager,
        )
        chunks_pages: list[list[Chunk]] = [[] for _ in range(num_pages)]
        for chunk in chunks:
            chunks_pages[chunk.metadata["page"] - 1].append(chunk)  # type: ignore

    return edit_positions_on_page(chunks_pages, extension), num_pages
