"""Extract subchunks from IPYNB file."""

import contextlib
from pathlib import Path
from typing import Any

import nbformat as nbf

from unichunking.tools import md_interpreter
from unichunking.types import (
    ChunkPosition,
    MatrixTable,
    SubChunk,
)


def extract_subchunks_ipynb(
    path: Path,
) -> tuple[list[SubChunk], list[MatrixTable], list[str]]:
    """Filetype-specific function : extracts subchunks from a IPYNB file.

    Keeps a typed-cells structure, with information on the programming language.
    (ex : "Cell 1 (Text) : ...", "Cell 2 (Code: python 3.11.7) : ...", "Output 1 of cell 2 : ...", "Output 2 of cell 2 : ...").

    Args:
        path: Path to the local file.

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

    notebook: Any = nbf.read(str(path), nbf.NO_CONVERT)  # type: ignore
    language = ""
    version = ""
    with contextlib.suppress(Exception):
        language = notebook.metadata.language_info.name
    with contextlib.suppress(Exception):
        version = notebook.metadata.language_info.version
    cells = notebook.cells

    for i_cell in range(len(cells)):
        match cells[i_cell].cell_type:
            case "markdown":
                subchunks.append(
                    SubChunk(
                        subchunk_id=len(subchunks),
                        content=f"** Cell {i_cell + 1} (Text) : ",
                        page=0,
                        position=ChunkPosition(0, 0, 0, 0),
                        file_name=filename,
                    ),
                )
                lines = cells[i_cell].source.split("\n")
                partial_subchunks, partial_tables, partial_images = md_interpreter(
                    lines,
                )

                for subchunk in partial_subchunks:
                    subchunk.subchunk_id = len(subchunks)
                    subchunk.file_name = filename
                    subchunks.append(subchunk)

                tables.extend(partial_tables)
                images.extend(partial_images)

                subchunks.append(
                    SubChunk(
                        subchunk_id=len(subchunks),
                        content=f" ; End of cell {i_cell + 1} ** ",
                        page=0,
                        position=ChunkPosition(0, 0, 0, 0),
                        file_name=filename,
                    ),
                )

            case "code":
                subchunks.append(
                    SubChunk(
                        subchunk_id=len(subchunks),
                        content=f"** Cell {i_cell + 1} (Code : {language} {version}) : ",
                        page=0,
                        position=ChunkPosition(0, 0, 0, 0),
                        file_name=filename,
                    ),
                )
                for line in cells[i_cell].source.split("\n"):
                    subchunks.append(
                        SubChunk(
                            subchunk_id=len(subchunks),
                            content=line + " ",
                            page=0,
                            position=ChunkPosition(0, 0, 0, 0),
                            file_name=filename,
                        ),
                    )
                subchunks.append(
                    SubChunk(
                        subchunk_id=len(subchunks),
                        content=f" ; End of cell {i_cell + 1} ** ",
                        page=0,
                        position=ChunkPosition(0, 0, 0, 0),
                        file_name=filename,
                    ),
                )
                for i_output in range(len(cells[i_cell].outputs)):
                    output_cell = cells[i_cell].outputs[i_output]
                    if output_cell.output_type != "stream":
                        continue
                    subchunks.append(
                        SubChunk(
                            subchunk_id=len(subchunks),
                            content=f"** Output {i_output + 1} of cell {i_cell + 1} : ",
                            page=0,
                            position=ChunkPosition(0, 0, 0, 0),
                            file_name=filename,
                        ),
                    )
                    for line in output_cell.text.split("\n"):
                        subchunks.append(
                            SubChunk(
                                subchunk_id=len(subchunks),
                                content=line + " ",
                                page=0,
                                position=ChunkPosition(0, 0, 0, 0),
                                file_name=filename,
                            ),
                        )
                    subchunks.append(
                        SubChunk(
                            subchunk_id=len(subchunks),
                            content=f" ; End of output {i_output + 1} of cell {i_cell + 1} ** ",
                            page=0,
                            position=ChunkPosition(0, 0, 0, 0),
                            file_name=filename,
                        ),
                    )

            case _:
                pass

    return subchunks, tables, images
