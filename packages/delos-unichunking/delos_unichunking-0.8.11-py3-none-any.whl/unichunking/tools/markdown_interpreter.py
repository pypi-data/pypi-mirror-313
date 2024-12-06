"""Reads MarkDown and identifies tables."""

from unichunking.settings import unisettings
from unichunking.types import ChunkPosition, MatrixTable, SubChunk


def md_interpreter(
    lines: list[str],
) -> tuple[list[SubChunk], list[MatrixTable], list[str]]:
    """Reads MarkDown with the ability to identify tables.

    Args:
        lines: Lines of text extracted from file.

    Returns:
        A tuple containing three lists:
        - List of subchunks, containing actual text or markers pointing to table/chart/image objects.
        - List of table/chart objects, of class MatrixTable.
        - List of image objects.
    """
    subchunks: list[SubChunk] = []
    tables: list[MatrixTable] = []
    images: list[str] = []

    i_line = 0
    while i_line < len(lines):
        if any(
            table_marker in lines[i_line]
            for table_marker in unisettings.text.TABLE_MARKERS
        ):
            if len(subchunks) > 0:
                subchunks.pop()
            table: list[list[str]] = []
            line_idx = i_line - 1
            while 0 <= line_idx < len(lines) and "|" in lines[line_idx]:
                if line_idx == i_line:
                    line_idx += 1
                    continue
                line_text = lines[line_idx].replace("\n", "").strip()
                line_content = line_text.split("|")
                if line_text[0] == "|":
                    line_content.pop(0)
                if line_text[-1].strip() == "|":
                    line_content.pop()
                table.append([cell.strip() for cell in line_content])
                line_idx += 1
            subchunks.append(
                SubChunk(
                    subchunk_id=0,
                    content=f"{len(tables)}",
                    page=0,
                    position=ChunkPosition(0, 0, 0, 0),
                    file_name="",
                    content_type="table",
                ),
            )
            tables.append(MatrixTable("", table))
            i_line = line_idx

        else:
            subchunk_content = lines[i_line].strip() + " "
            if subchunk_content:
                subchunks.append(
                    SubChunk(
                        subchunk_id=0,
                        content=subchunk_content + " ",
                        page=0,
                        position=ChunkPosition(0, 0, 0, 0),
                        file_name="",
                    ),
                )
            i_line += 1

    return subchunks, tables, images
