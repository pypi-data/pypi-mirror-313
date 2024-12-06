"""Functions to extract data from XML structures."""

from pathlib import Path
from zipfile import ZipFile

from unichunking.types import MatrixTable


def _clean_xml(string: str) -> str:
    return (
        string.replace("\\xc3\\xa9", "é").replace("&apos;", "'").replace("&#10;", "\n")
    )


def _extract_charts_xml(
    file_path: Path,
    element_xml: str,
    extension: str,
    page_idx: int,
) -> list[str]:
    """Extracts the XML encoding of a chart in a DOCX/PPTX file.

    Args:
        file_path: Path to the local file.
        element_xml: XML encoding of the element pointing to the chart in the file.
        extension: File extension.
        page_idx: Index of the page containing the chart in the file.

    Returns:
        A list of length 1 (for compatibility reasons) containing the XML encoding of the chart.
    """
    with file_path.open("rb") as doc:
        zip_doc = ZipFile(doc)

        if extension == "docx":
            app = "word"
            rel_path = "word/_rels/document.xml.rels"

        else:
            app = "ppt"
            rel_path = f"ppt/slides/_rels/slide{page_idx}.xml.rels"

        element_charts = element_xml.split('r:id="rId')[1:]
        charts_ids = [element_chart.split('"/>')[0] for element_chart in element_charts]
        charts_paths = [
            (
                str(zip_doc.read(rel_path))
                .split(f'<Relationship Id="rId{chart_id}"')
                .pop()
                .split('"/>')[0]
                .split('Target="')
                .pop()
            ).replace("../", "")
            for chart_id in charts_ids
        ]

        return [
            str(
                zip_doc.read(
                    f"{app}/{chart_path}",
                ),
            )
            for chart_path in charts_paths
        ]


def extract_charts(
    file_path: Path,
    element_xml: str,
    extension: str,
    page_idx: int = 0,
    charts_xml: list[str] | None = None,
) -> list[MatrixTable]:
    """Extracts the data of Office charts from their XML encoding.

    Args:
        file_path: Path to the local file.
        element_xml: XML encoding of the element pointing to the chart in the file.
        extension: File extension.
        page_idx: Index of the page containing the chart in the file.
        charts_xml: A list containing the XML encodings of all charts to process.

    Returns:
        A list of chart objects, of class MatrixTable.
    """
    if charts_xml is None:
        charts_xml = _extract_charts_xml(
            file_path=file_path,
            element_xml=element_xml,
            extension=extension,
            page_idx=page_idx,
        )

    tables: list[MatrixTable] = []

    for chart_xml in charts_xml:
        title = chart_xml.split("<a:t>").pop().split("</a:t>")[0]
        title = (title != chart_xml) * _clean_xml(title)

        plots = chart_xml.split("<c:plotArea>")
        plots.pop(0)

        for plot in plots:
            table = [[""]]
            categories = (
                plot.split("<c:strCache>")
                .pop()
                .split("</c:strCache>")[0]
                .split("<c:v>")
            )
            for category in categories[1:]:
                table[0].append(_clean_xml(category.split("</c:v>")[0]))
            series = plot.split("<c:strCache>")
            for i_series in range(1, len(series)):
                if i_series % 2:
                    table.append(
                        [
                            _clean_xml(
                                series[i_series]
                                .split("<c:v>")
                                .pop()
                                .split("</c:v>")[0],
                            ),
                        ],
                    )
                else:
                    table[-1].extend(
                        [
                            value.split("</c:v>")[0]
                            for value in series[i_series]
                            .split("</c:strCache")
                            .pop()
                            .split("<c:v>")[1:]
                        ],
                    )

            tables.append(MatrixTable(title, table, is_chart=True))

    return tables


def extract_media_xlsx(
    file_path: Path,
    page_idx: int,
) -> tuple[list[MatrixTable], list[bytes]]:
    """Extracts all charts and images on a given sheet of an XLSX file.

    Args:
        file_path: Path to the local file.
        page_idx: Index of the sheet to process.

    Returns:
        A tuple containing two lists:
        - List of table/chart objects.
        - List of image objects.
    """
    charts_xml: list[str] = []
    images: list[bytes] = []

    with file_path.open("rb") as doc:
        zip_doc = ZipFile(doc)

        drawings_rels = str(zip_doc.read(f"xl/worksheets/sheet{page_idx}.xml")).split(
            '<drawing r:id="rId',
        )[1:]
        if not drawings_rels:
            return [], []
        sheet_rels = str(zip_doc.read(f"xl/worksheets/_rels/sheet{page_idx}.xml.rels"))

        drawings: list[str] = []
        for drawing_rel in drawings_rels:
            drawing_rid = drawing_rel.split('"/>')[0]
            drawings.append(
                sheet_rels.split(f'<Relationship Id="rId{drawing_rid}')
                .pop()
                .split('"/>')[0]
                .split('Target="../drawings/')
                .pop(),
            )

        for drawing in drawings:
            drawing_xml = str(zip_doc.read(f"xl/drawings/{drawing}"))
            drawing_rels = str(zip_doc.read(f"xl/drawings/_rels/{drawing}.rels"))

            drawing_charts = drawing_xml.split(
                "<c:chart ",
            )[1:]
            charts_rid = [
                chart.split('r:id="rId')[1].split('"/>')[0] for chart in drawing_charts
            ]
            charts_paths = [
                drawing_rels.split(f'<Relationship Id="rId{chart_rid}')
                .pop()
                .split('Target="../')[1]
                .split('"/>')[0]
                for chart_rid in charts_rid
            ]
            charts_xml.extend(
                [str(zip_doc.read(f"xl/{chart_path}")) for chart_path in charts_paths],
            )

            drawing_images = drawing_xml.split(
                '<a:blip r:embed="rId',
            )[1:]
            images_rid = [image.split('">')[0] for image in drawing_images]
            images_paths = [
                drawing_rels.split(f'<Relationship Id="rId{image_rid}')
                .pop()
                .split('Target="../')[1]
                .split('"/>')[0]
                for image_rid in images_rid
            ]
            images.extend(
                [zip_doc.read(f"xl/{image_path}") for image_path in images_paths],
            )

        return (
            extract_charts(
                file_path=file_path,
                element_xml="",
                extension="xlsx",
                page_idx=page_idx,
                charts_xml=charts_xml,
            ),
            images,
        )
