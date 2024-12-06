"""Extract subchunks from TXT/CSV/MD file."""

from pathlib import Path

from unichunking.tools import md_interpreter
from unichunking.types import (
    ChunkPosition,
    MatrixTable,
    SubChunk,
)


def extract_subchunks_txt(
    path: Path,
    is_csv: bool = False,
) -> tuple[list[SubChunk], list[MatrixTable], list[str]]:
    """Filetype-specific function : extracts subchunks from a TXT/MD/CSV file.

    Args:
        path: Path to the local file.
        is_csv: Boolean marker indicating whether file must be read as a CSV table.

    Returns:
        A tuple containing three lists:
        - List of subchunks, containing actual text or markers pointing to table/chart/image objects.
        - List of table/chart objects, of class MatrixTable.
        - List of image objects.
    """
    filename = path.name

    subchunks: list[SubChunk] = []
    tables: list[MatrixTable] = []
    images: list[str] = []

    if is_csv:
        table: list[list[str]] = []
        with path.open() as file:
            for line in file:
                line_values: list[str] = []
                cur_value = ""
                in_str = False
                line.replace("\n", "")
                for i in range(len(line)):
                    if line[i] == '"':
                        in_str = not in_str
                    elif line[i] == "," and not in_str:
                        line_values.append(cur_value)
                        cur_value = ""
                    else:
                        cur_value += line[i]
                line_values.append(cur_value)
                table.append(line_values)
        subchunks.append(
            SubChunk(
                subchunk_id=len(subchunks),
                content="0",
                page=0,
                position=ChunkPosition(0, 0, 0, 0),
                file_name=filename,
                content_type="table",
            ),
        )
        tables.append(MatrixTable("", table))

    else:
        with path.open() as file:
            lines = file.readlines()
            partial_subchunks, tables, images = md_interpreter(lines)
            for subchunk in partial_subchunks:
                subchunk.subchunk_id = len(subchunks)
                subchunk.file_name = filename
                subchunks.append(subchunk)

    return subchunks, tables, images
