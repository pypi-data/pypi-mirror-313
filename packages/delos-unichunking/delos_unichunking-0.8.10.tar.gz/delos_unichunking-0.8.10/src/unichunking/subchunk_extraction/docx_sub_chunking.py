"""Extract subchunks from DOCX file."""

import base64
import re
from pathlib import Path
from typing import Any, Callable

from docx import Document
from docx.oxml import parse_xml
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

from unichunking.tools import (
    compact_matrix,
    convert_file,
    extract_charts,
)
from unichunking.types import (
    ChunkPosition,
    MatrixTable,
    SubChunk,
)
from unichunking.utils import logger


def _format_toc(toc: list[tuple[str, str]]) -> str:
    text = "Table of content : \n\n\n"

    for number, title in toc:
        try:
            num = int(number)
        except Exception:  # noqa: BLE001, S112
            continue

        text += f"{'#' * num} {title}\n"

    return text


def _extract_toc(para_xml: str) -> tuple[str, str]:
    p = parse_xml(para_xml)
    p_style_val = p.xpath(".//w:pStyle/@w:val")
    if len(p_style_val) > 0:
        title = p_style_val[0]
        numbers = re.findall(r"\d+", title)
        if numbers:
            number = "".join(numbers)
        else:
            return "", ""
    else:
        return "", ""

    w_t_texts = p.xpath(".//w:t/text()")
    w_t_text_combined = ""
    if w_t_texts:
        w_t_text_combined = "".join(w_t_texts)

    return number, w_t_text_combined


def _docx_to_matrixtable(elt: Table) -> MatrixTable:
    matrix_table: list[list[str]] = []
    for row in elt.rows:
        cur_line = [
            cell.text.replace("\n", " ").replace("\xa0", " ") for cell in row.cells
        ]
        matrix_table.append(cur_line)
    return MatrixTable("", matrix_table)


def _compute_position(section: Any) -> ChunkPosition:
    position = ChunkPosition(0, 0, 1, 1)

    if section.page_width:
        if section.left_margin:
            position.x0 = section.left_margin.inches / section.page_width.inches
        if section.right_margin:
            position.x1 = 1 - section.right_margin.inches / section.page_width.inches
    if section.page_height:
        if section.top_margin:
            position.y0 = section.top_margin.inches / section.page_height.inches
        if section.bottom_margin:
            position.y1 = 1 - section.bottom_margin.inches / section.page_height.inches

    return position


def _heading_paragraph(
    para: Paragraph,
    position: ChunkPosition,
    subchunks: list[SubChunk],
    cur_page: int,
    filename: str,
) -> tuple[list[SubChunk], int]:
    for run in para.runs:
        if "lastRenderedPageBreak" in run.element.xml or (
            "w:br" in run.element.xml and 'type="page"' in run.element.xml
        ):
            cur_page += 1
        text = run.text
        if run.font.bold:
            text = f"**{text}**"
        subchunks.append(
            SubChunk(
                subchunk_id=len(subchunks),
                content=text + " ",
                page=cur_page,
                position=position,
                file_name=filename,
            ),
        )

    return subchunks, cur_page


def _checkbox_paragraph(
    para: Paragraph,
    p: Any,
    position: ChunkPosition,
    subchunks: list[SubChunk],
    cur_page: int,
    filename: str,
) -> tuple[list[SubChunk], int]:
    seq = """<w:default w:val="1"/>"""

    if seq in p.xml:
        for run in para.runs:
            if "lastRenderedPageBreak" in run.element.xml or (
                "w:br" in run.element.xml and 'type="page"' in run.element.xml
            ):
                cur_page += 1
        subchunks.append(
            SubChunk(
                subchunk_id=len(subchunks),
                content="- [X]" + para.text + " ",
                page=cur_page,
                position=position,
                file_name=filename,
            ),
        )
    else:
        for run in para.runs:
            if "lastRenderedPageBreak" in run.element.xml or (
                "w:br" in run.element.xml and 'type="page"' in run.element.xml
            ):
                cur_page += 1
        subchunks.append(
            SubChunk(
                subchunk_id=len(subchunks),
                content="- [ ]" + para.text + " ",
                page=cur_page,
                position=position,
                file_name=filename,
            ),
        )

    return subchunks, cur_page


def _list_paragraph(
    para: Paragraph,
    position: ChunkPosition,
    subchunks: list[SubChunk],
    cur_page: int,
    filename: str,
) -> tuple[list[SubChunk], int]:
    for run in para.runs:
        if "lastRenderedPageBreak" in run.element.xml or (
            "w:br" in run.element.xml and 'type="page"' in run.element.xml
        ):
            cur_page += 1
        espaces_indentation = ""
        if para.paragraph_format.left_indent:
            espaces_indentation = " " * 4
            subchunks.append(
                SubChunk(
                    subchunk_id=len(subchunks),
                    content=espaces_indentation + "- " + para.text.strip() + " ",
                    page=cur_page,
                    position=position,
                    file_name=filename,
                ),
            )
        else:
            subchunks.append(
                SubChunk(
                    subchunk_id=len(subchunks),
                    content="* " + para.text + "\n",
                    page=cur_page,
                    position=position,
                    file_name=filename,
                ),
            )
    return subchunks, cur_page


def _toc_paragraph(
    para: Paragraph,
    position: ChunkPosition,
    subchunks: list[SubChunk],
    cur_page: int,
    filename: str,
) -> tuple[list[SubChunk], int]:
    if (
        para.style is not None
        and para.style.name is not None
        and "TOC" in para.style.name
    ):
        text = para.text
        if text:
            subchunks.append(
                SubChunk(
                    subchunk_id=len(subchunks),
                    content=f"Table des matières : {text}",
                    page=cur_page,
                    position=position,
                    file_name=filename,
                ),
            )
    return subchunks, cur_page


def _handle_paragraph(
    para: Paragraph,
    para_xml: str,
    position: ChunkPosition,
    subchunks: list[SubChunk],
    cur_page: int,
    filename: str,
    image_rels: dict[str, str],
) -> tuple[list[SubChunk], int]:
    p = parse_xml(para_xml)

    if para.style and para.style.name and para.style.name.lower().startswith("toc"):
        subchunks, cur_page = _toc_paragraph(
            para=para,
            position=position,
            subchunks=subchunks,
            cur_page=cur_page,
            filename=filename,
        )

    elif para.style and para.style.name and para.style.name.startswith("Heading"):
        subchunks, cur_page = _heading_paragraph(
            para=para,
            position=position,
            subchunks=subchunks,
            cur_page=cur_page,
            filename=filename,
        )

    elif p.xpath(".//w:checkBox") != []:
        subchunks, cur_page = _checkbox_paragraph(
            para=para,
            p=p,
            position=position,
            subchunks=subchunks,
            cur_page=cur_page,
            filename=filename,
        )

    elif para.style and para.style.name == "List Paragraph":
        subchunks, cur_page = _list_paragraph(
            para=para,
            position=position,
            subchunks=subchunks,
            cur_page=cur_page,
            filename=filename,
        )

    else:
        for run in para.runs:
            if "lastRenderedPageBreak" in run.element.xml:
                cur_page += 1

            text = run.text
            if run.font.bold:
                text = f"**{text}**"
            subchunks.append(
                SubChunk(
                    subchunk_id=len(subchunks),
                    content=text.replace("\t", " ") + " ",
                    page=cur_page,
                    position=position,
                    file_name=filename,
                ),
            )

    for drawing in p.xpath(".//w:drawing//a:blip"):
        rid = drawing.get(qn("r:embed"))
        if rid in image_rels:
            subchunks.append(
                SubChunk(
                    subchunk_id=len(subchunks),
                    content=image_rels[rid],
                    page=cur_page,
                    position=position,
                    file_name=filename,
                    content_type="image",
                ),
            )

    return subchunks, cur_page


def extract_subchunks_docx(  # noqa: C901, PLR0912
    path: Path,
    extension: str,
    function: Callable[[str], str],
) -> tuple[list[SubChunk], list[MatrixTable], list[str], Path]:
    """Filetype-specific function : extracts subchunks from a DOCX file.

    For DOC & ODT : local file converted to DOCX, subchunks extracted from DOCX.
    Detects any potential page breaks left by renderers to help with further page computing.

    Args:
        path: Path to the local file.
        extension: File extension.
        function: Function to handle images.

    Returns:
        A tuple containing three lists and a Path:
        - List of subchunks, containing actual text or markers pointing to table/chart/image objects.
        - List of table/chart objects, of class MatrixTable.
        - List of image objects.
        - Path to the processed DOCX file, different from the initial path if a conversion occured.
    """
    subchunks: list[SubChunk] = []
    tables: list[MatrixTable] = []
    images: list[str] = []

    filename = path.name

    if extension != "docx":
        path = convert_file(path, "docx")

    doc = Document(str(path))

    toc: list[tuple[str, str]] = []

    img_idx = 0
    image_rels: dict[str, str] = {}
    for rel in doc.part.rels.values():
        if "image" in rel.reltype:
            try:
                image_part = rel.target_part
                image_bytes = image_part.blob
                base64_image = base64.b64encode(image_bytes).decode("utf-8")
                image_description = function(base64_image)
                image_rels[rel.rId] = f"{img_idx}"
                images.append(image_description)
                img_idx += 1
            except Exception as e:  # noqa: BLE001
                logger.debug(f"Image couldn't be processed : {e}")

    cur_page = 0

    for section in doc.sections:
        position = _compute_position(section)

        for elt in section.iter_inner_content():
            if isinstance(elt, Paragraph):
                para_xml = elt._p.xml  # type: ignore # noqa: SLF001
                if 'w:name="_Toc' in para_xml:
                    number, title = _extract_toc(
                        para_xml=para_xml,
                    )
                    if number and title:
                        toc.append((number, title))

                if "<c:chart " in para_xml:
                    for plot in extract_charts(
                        file_path=path,
                        element_xml=para_xml,
                        extension="docx",
                    ):
                        subchunks.append(
                            SubChunk(
                                subchunk_id=len(subchunks),
                                content=f"{len(tables)}",
                                page=cur_page,
                                position=position,
                                file_name=filename,
                                content_type="table",
                            ),
                        )
                        tables.append(plot)

                subchunks, cur_page = _handle_paragraph(
                    para=elt,
                    para_xml=para_xml,
                    position=position,
                    subchunks=subchunks,
                    cur_page=cur_page,
                    filename=filename,
                    image_rels=image_rels,
                )

            else:
                table = compact_matrix(table=_docx_to_matrixtable(elt))
                if table.abort():
                    subchunks.append(
                        SubChunk(
                            subchunk_id=len(subchunks),
                            content=table.read_as_str(),
                            page=cur_page,
                            position=position,
                            file_name=filename,
                        ),
                    )
                else:
                    subchunks.append(
                        SubChunk(
                            subchunk_id=len(subchunks),
                            content=f"{len(tables)}",
                            page=cur_page,
                            position=position,
                            file_name=filename,
                            content_type="table",
                        ),
                    )
                    tables.append(table)

    toc_text = _format_toc(toc)

    subchunks.append(
        SubChunk(
            subchunk_id=len(subchunks),
            content=toc_text,
            page=1,
            position=ChunkPosition(0, 0, 1, 1),
            file_name=filename,
            content_type="text",
        ),
    )

    subchunks = [s for s in subchunks if s.content.strip()]

    return subchunks, tables, images, path
