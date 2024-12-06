"""Extract subchunks from PDF file."""

import base64
import operator
from functools import reduce
from pathlib import Path
from typing import Any, Callable, List, Tuple

import fitz
import pymupdf

from unichunking.types import ChunkPosition, SubChunk
from unichunking.utils import logger

MIN_PIXELS: int = 128


def _handle_line(
    line: Any,
    width: float,
    height: float,
    subchunk_idx: int,
    page_num: int,
    file_name: str,
) -> Tuple[List[SubChunk], int]:
    line_chunks: List[SubChunk] = []
    for span in line["spans"]:
        text = str(span["text"].replace("�", " ").strip())
        font: Any = span["font"]
        bbox: Any = span["bbox"]
        if "bold" in font.lower():
            text = f"**{text}**"
        if text:
            x0, y0, x1, y1 = bbox
            position = ChunkPosition(
                x0=x0 / width,
                y0=y0 / height,
                x1=x1 / width,
                y1=y1 / height,
            )
            line_chunks.append(
                SubChunk(
                    subchunk_id=subchunk_idx,
                    content=text,
                    page=page_num,
                    position=position,
                    file_name=file_name,
                ),
            )
            subchunk_idx += 1

    return line_chunks, subchunk_idx


async def _retrieve_subchunks(  # noqa: C901, PLR0915
    path: Path,
    status_manager: Any,
    function: Callable[[str], str],
) -> Tuple[List[List[List[List[SubChunk]]]], List[SubChunk]]:
    chunks: List[List[List[List[SubChunk]]]] = []
    images_chunks: List[SubChunk] = []
    idx = 0
    image_idx = 0
    old_count = 0

    with pymupdf.Document(path) as doc:
        num_pages: Any = doc.page_count  # type: ignore
        for page_num in range(num_pages):
            # text
            if page_num % int(num_pages / 17 + 1) == 0:
                page_progress = int((page_num + 1) / num_pages * 75)
                await status_manager.update_status(
                    progress=page_progress,
                    start=status_manager.start,
                    end=status_manager.end,
                )
            page_chunks: List[List[List[SubChunk]]] = []
            textpage: Any = doc.load_page(page_num).get_textpage()  # type: ignore
            page = textpage.extractDICT(sort=False)
            width, height = page["width"], page["height"]
            blocks = page["blocks"]

            for block in blocks:
                block_chunks: List[List[SubChunk]] = []
                lines = block["lines"]
                for line in lines:
                    line_chunks, idx = _handle_line(
                        line=line,
                        width=width,
                        height=height,
                        subchunk_idx=idx,
                        page_num=page_num,
                        file_name=path.name,
                    )
                    if line_chunks:
                        block_chunks.append(line_chunks)
                if block_chunks:
                    page_chunks.append(block_chunks)
            if page_chunks:
                chunks.append(page_chunks)

            # image
            doc_page = doc.load_page(page_num)  # type: ignore
            for image in doc_page.get_images(full=True):  # type: ignore
                rect = doc_page.get_image_bbox(image)  # type: ignore
                x0, y0, x1, y1 = rect.x0, rect.y0, rect.x1, rect.y1  # type: ignore
                image_width, image_height = int(image[2]), int(image[3])  # type: ignore

                if image_width >= MIN_PIXELS and image_height >= MIN_PIXELS:
                    image_bytes = doc.extract_image(image[0])["image"]  # type: ignore
                    try:
                        base64_image = base64.b64encode(image_bytes).decode("utf-8")  # type: ignore
                        image_description = function(base64_image)
                        image_chunk = SubChunk(
                            subchunk_id=7_700_000 + image_idx,
                            content=image_description,
                            page=page_num,
                            position=ChunkPosition(
                                x0=x0 / width,  # type: ignore
                                y0=y0 / height,  # type: ignore
                                x1=x1 / width,  # type: ignore
                                y1=y1 / height,  # type: ignore
                            ),
                            file_name=path.name,
                            content_type="image",
                        )
                        image_idx += 1
                        images_chunks.append(image_chunk)
                    except Exception as e:  # noqa: BLE001
                        logger.debug(f"Image couldn't be processed : {e}")

            if old_count == idx + image_idx:  # nothing was found on the page!
                logger.debug(f"Nothing was found on page {page_num} --> ScreenShot")
                zoom = 1.0  # Modifier le facteur de zoom pour une meilleure qualité
                mat = fitz.Matrix(zoom, zoom)

                # Convertir la page en image pixmap
                page = doc.load_page(page_num)  # type: ignore
                pix = page.get_pixmap(matrix=mat)  # type: ignore
                image_bytes = pix.tobytes()  # type: ignore

                base64_image = base64.b64encode(image_bytes).decode("utf-8")  # type: ignore
                image_description = function(base64_image)
                image_chunk = SubChunk(
                    subchunk_id=7_700_000 + image_idx,
                    content=image_description,
                    page=page_num,
                    position=ChunkPosition(
                        x0=0,
                        y0=0,
                        x1=1,
                        y1=1,
                    ),
                    file_name=path.name,
                    content_type="image",
                )
                image_idx += 1
                images_chunks.append(image_chunk)

            old_count = image_idx + idx

    return chunks, images_chunks


def _filter_subchunks(
    chunks: List[List[List[List[SubChunk]]]],
) -> List[SubChunk]:
    flattened_chunks: List[SubChunk] = []

    for page_chunks in chunks:
        for block_chunks in page_chunks:
            for line_chunks in block_chunks:
                if line_chunks:
                    filtered_line_chunks = reduce(operator.add, line_chunks)
                    flattened_chunks.append(filtered_line_chunks)

    return flattened_chunks


async def extract_subchunks_pdf(
    path: Path,
    status_manager: Any,
    function: Callable[[str], str],
) -> List[SubChunk]:
    """Filetype-specific function : extracts subchunks from a PDF file.

    Args:
        path: Path to the local file.
        status_manager: Optional, special object to manage task progress.
        function: Function to handle images.

    Returns:
        A list of SubChunk objects.
    """
    chunks, images_chunks = await _retrieve_subchunks(
        path=path,
        status_manager=status_manager,
        function=function,
    )
    flattened_chunks = _filter_subchunks(chunks)

    flattened_chunks.extend(images_chunks)

    progress = 100
    await status_manager.update_status(
        progress=progress,
        start=status_manager.start,
        end=status_manager.end,
    )

    return flattened_chunks
