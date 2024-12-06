"""Subchunk extraction and formating for any file type."""

from pathlib import Path
from typing import Any, Callable

from llmax import tokens

from unichunking.settings import unisettings
from unichunking.subchunk_extraction import (
    extract_subchunks_docx,
    extract_subchunks_ipynb,
    extract_subchunks_pdf,
    extract_subchunks_pptx,
    extract_subchunks_txt,
    extract_subchunks_xlsx,
)
from unichunking.types import MatrixTable, StatusManager, SubChunk
from unichunking.utils import logger


def _compute_page_num(
    cur_page_num: int,
    cur_page_size: int,
    subchunk_page: int,
    fake_pages_length: int,
) -> int:
    if fake_pages_length:
        return cur_page_num + (cur_page_size > fake_pages_length)
    return subchunk_page


def _split_table(
    table: MatrixTable,
    size_threshold: int,
) -> tuple[MatrixTable, MatrixTable]:
    table_matrix = table.content
    table_title = table.title

    sub_tab_1, sub_tab_2 = [], []

    first_line = table_matrix[0]
    sub_tab_1 = table_matrix[:2]
    split_after_line = 2
    while (
        tokens.count(str(table_matrix[: split_after_line + 1])) < size_threshold
        and split_after_line < len(table_matrix) - 1
    ):
        sub_tab_1 = table_matrix[: split_after_line + 1]
        split_after_line += 1
    sub_tab_2 = [first_line] + table_matrix[split_after_line:]

    return MatrixTable(table_title, sub_tab_1), MatrixTable(table_title, sub_tab_2)


def _format_table(
    table: MatrixTable,
    chunk_size: int,
    k_max: int,
    min_format: int = 2,
) -> list[str]:
    """Splits a table to fit in the k_max format.

    Keeps the columns/lines information on all subtables to avoid information loss.

    Args:
        table: MatrixTable object to split.
        chunk_size: Size of the current chunk without the table, in tokens.
        k_max: Maximum chunk size, in tokens.
        min_format: Minimum number of lines to keep in a subtable.

    Returns:
        A list of strings representing the subtables created.
    """
    if tokens.count(str(table.read())) + chunk_size <= k_max:
        return [table.read()]

    end_of_cur_chunk, leftover = _split_table(table, size_threshold=k_max - chunk_size)
    tables_done = [end_of_cur_chunk.read()]
    tables_temp = [leftover]

    while len(tables_temp) > 0:
        cur_table = tables_temp.pop()
        cur_table_str = cur_table.read()

        if cur_table.abort():
            tables_done.append(cur_table.read_as_str())

        elif (
            max(len(cur_table.content), len(cur_table.content[0])) <= min_format
            or tokens.count(cur_table_str) <= k_max
        ):
            tables_done.append(cur_table.read())

        else:
            sub_tab_1, sub_tab_2 = _split_table(cur_table, size_threshold=k_max)
            tables_done.append(sub_tab_1.read())
            tables_temp.append(sub_tab_2)

    return tables_done


async def _format_subchunks(
    subchunks: list[SubChunk],
    tables: list[MatrixTable],
    images: list[str],
    k_max: int,
    fake_pages_length: int,
    status_manager: Any = None,
) -> list[SubChunk]:
    """Processes the items extracted by filetype-specific functions to return SubChunks.

    Replaces markers to table/chart/image objects by the corresponding objects.
    Imposes k_max format by splitting subchunks of exceeding length.
    Handles artifical pagination for file types without clear page definition.

    Args:
        subchunks: List of subchhunks extracted by filetype-specific function.
        tables: List of table/chart objects extracted by filetype-specific function.
        images: List of image objects extracted by filetype-specific function.
        k_max: Maximum chunk size, in tokens.
        fake_pages_length: Maximum page size, in tokens, for file types without clear page definition.
        status_manager: Optional, special object to manage task progress.

    Returns:
        A list of SubChunk objects.
    """
    if fake_pages_length:
        logger.debug("Adding artificial page numbers.")

    chunks: list[SubChunk] = []
    cur_page_size = 0
    cur_page_num = 0
    subchunks_progress = 0

    for i_subchunk in range(len(subchunks)):
        new_progress = (int((i_subchunk + 1) / len(subchunks) * 100 / 5)) * 5
        if new_progress > subchunks_progress:
            subchunks_progress = new_progress
            await status_manager.update_status(
                progress=subchunks_progress,
                start=status_manager.start,
                end=status_manager.end,
            )

        subchunk_content = subchunks[i_subchunk].content
        subchunk_content_type = subchunks[i_subchunk].content_type

        match subchunk_content_type:
            case "table":
                table = tables[int(subchunk_content)]
                formatted_tables = _format_table(
                    table=table,
                    chunk_size=0,
                    k_max=k_max,
                )
                subchunk_content = formatted_tables.pop()
                for formatted_table in formatted_tables:
                    new_page_num = _compute_page_num(
                        cur_page_num=cur_page_num,
                        cur_page_size=cur_page_size,
                        subchunk_page=subchunks[i_subchunk].page,
                        fake_pages_length=fake_pages_length,
                    )
                    chunks.append(
                        SubChunk(
                            subchunk_id=len(chunks),
                            content=formatted_table,
                            page=new_page_num,
                            position=subchunks[i_subchunk].position,
                            file_name=subchunks[i_subchunk].file_name,
                            content_type="table",
                        ),
                    )
                    if new_page_num > cur_page_num:
                        cur_page_size = 0
                    cur_page_size += tokens.count(formatted_table)
                    cur_page_num = new_page_num

            case "image":
                subchunk_content = images[int(subchunk_content)]

            case _:
                pass

        if subchunk_content.strip():
            new_page_num = _compute_page_num(
                cur_page_num=cur_page_num,
                cur_page_size=cur_page_size,
                subchunk_page=subchunks[i_subchunk].page,
                fake_pages_length=fake_pages_length,
            )
            chunks.append(
                SubChunk(
                    subchunk_id=len(chunks),
                    content=subchunk_content,
                    page=new_page_num,
                    position=subchunks[i_subchunk].position,
                    file_name=subchunks[i_subchunk].file_name,
                    content_type=subchunks[i_subchunk].content_type,
                ),
            )
            if new_page_num > cur_page_num:
                cur_page_size = 0
            cur_page_size += tokens.count(chunks[-1].content)
            cur_page_num = new_page_num

    return chunks


async def extract_subchunks(
    path: Path,
    function: Callable[[str], str],
    k_max: int = unisettings.chunking.DEFAULT_K_MAX,
    status_manager: Any = None,
) -> list[SubChunk]:
    """Global function that extracts chunks from any document.

    Args:
        path: Path to the local file.
        function: Function to describe images
        k_max: Maximum chunk size, in tokens.
        status_manager: Optional, special object to manage task progress.

    Returns:
        A list of SubChunk objects.
    """
    if not status_manager:
        status_manager = StatusManager(task="Subchunk extraction")

    new_path = path
    extension = path.suffix[1:].lower()

    if extension == "pdf":
        formatted_subchunks = await extract_subchunks_pdf(
            path,
            status_manager=status_manager,
            function=function,
        )

    else:
        subchunks, tables, images = [], [], []
        fake_pages_length = unisettings.chunking.FAKE_PAGES_LENGTH

        match extension:
            case "docx" | "doc" | "odt":
                subchunks, tables, images, new_path = extract_subchunks_docx(
                    path,
                    extension,
                    function=function,
                )
                extension = "docx"
                fake_pages_length = 0

            case "xlsx" | "xls" | "ods":
                subchunks, tables, images, new_path = extract_subchunks_xlsx(
                    path,
                    extension,
                )

            case "pptx" | "ppt" | "odp":
                subchunks, tables, images, new_path = extract_subchunks_pptx(
                    path,
                    extension,
                    function=function,
                )
                fake_pages_length = 0

            case "txt" | "md" | "csv":
                subchunks, tables, images = extract_subchunks_txt(
                    path,
                    is_csv=extension == "csv",
                )

            case "ipynb":
                subchunks, tables, images = extract_subchunks_ipynb(path)

            case _:
                pass

        if new_path != path:
            new_path.unlink()
            logger.debug(
                "Deleted local converted file.",
            )

        formatted_subchunks = await _format_subchunks(
            subchunks=subchunks,
            tables=tables,
            images=images,
            k_max=k_max,
            fake_pages_length=fake_pages_length,
            status_manager=status_manager,
        )

    subchunks_final: list[SubChunk] = []

    for subchunk in formatted_subchunks:
        ct = subchunk.content
        ct = (
            ct.replace("\uf0b7", " ")
            .replace("\xe0", "à")
            .replace("\xe7", "ç")
            .replace("\xe8", "è")
            .replace("\xf4", "ô")
            .replace("\xe9", "é")
        )
        ct = ct.replace("\n", " ")
        ct = ct.replace("   ", " ")
        subchunks_final.append(
            SubChunk(
                subchunk_id=subchunk.subchunk_id,
                content=ct,
                page=subchunk.page,
                position=subchunk.position,
                file_name=subchunk.file_name,
                content_type=subchunk.content_type,
            ),
        )

    logger.debug(
        "Subchunks extraction done.",
    )

    return subchunks_final
