"""Algorithmic correction/processing of table structures."""

from unichunking.types import MatrixTable

list_of_known_units = ["", "€", "$", "£", "%", "(", ")", "[", "]", "{", "}", "/", "."]


def _clean_cell(cell: str) -> str:
    return (
        cell.replace(" ", "").replace("\n", "").replace("\xa0", "").replace("None", "")
    )


def _check_if_splitted_cell(table: MatrixTable) -> bool:
    """Identifies if the input table contains a single value, in which case it is probably the result of splitting a merged cell during XLSX processing."""
    value = ""
    found_something = False
    table_matrix = table.content
    for i in range(len(table_matrix)):
        for j in range(len(table_matrix[i])):
            if table_matrix[i][j] != value:
                if found_something:
                    return False
                value = table_matrix[i][j]
                found_something = True
    table.content = [[value]]
    return True


def _square_format(table: MatrixTable) -> bool:
    """If the table is not rectangular, adds empty cells to avoid index errors."""
    matrix_table = table.content
    for i in range(len(matrix_table)):
        for j in range(len(matrix_table[i])):
            temp = _clean_cell(matrix_table[i][j])
            if temp in list_of_known_units:
                matrix_table[i][j] = temp
        while len(matrix_table[i]) < len(matrix_table[0]):
            matrix_table[i].append("")
    table.content = matrix_table
    return True


def _delete_empty_lines(table: MatrixTable) -> bool:
    matrix_table = table.content
    for i in range(len(matrix_table) - 1, -1, -1):
        if not table.abort():
            is_empty_line = True
            j = 0
            while j < len(matrix_table[i]) and is_empty_line:
                is_empty_line = is_empty_line and not matrix_table[i][j]
                j += 1
            if is_empty_line:
                matrix_table.pop(i)
        else:
            break
        table.content = matrix_table
    return True


def _delete_empty_columns(table: MatrixTable) -> bool:
    matrix_table = table.content
    for j in range(len(matrix_table[0]) - 1, -1, -1):
        if not table.abort():
            is_empty_column = True
            i = 0
            while i < len(matrix_table) and is_empty_column:
                is_empty_column = is_empty_column and not matrix_table[i][j]
                i += 1
            if is_empty_column:
                for i in range(len(matrix_table)):
                    matrix_table[i].pop(j)
        else:
            break
        table.content = matrix_table
    return True


def _extract_title(table: MatrixTable) -> bool:
    """A first line that only contains 1 non-empty value (potentially repeated) is the result of python-docx splitting the table title in cells.

    Can be spread on multiple lines, hence the iteration.
    """
    matrix_table = table.content
    title_done = False
    while not (title_done or table.abort()):
        changed_something = False
        title = ""
        for j in range(len(matrix_table[0])):
            if matrix_table[0][j] not in {"", title}:
                if title:
                    changed_something = False
                    title_done = True
                    break
                title = matrix_table[0][j]
                changed_something = True
        title_done = title_done or not changed_something
        if changed_something or not title:
            table.title += title
            matrix_table.pop(0)
            table.content = matrix_table
        matrix_table = table.content
    table.content = matrix_table
    return not table.abort()


def _merge_lines(table: MatrixTable, base_line: int, added_line: int) -> bool:
    if not table.abort():
        matrix_table = table.content
        for k in range(len(matrix_table[base_line])):
            if matrix_table[base_line][k] != matrix_table[added_line][k]:
                matrix_table[base_line][k] += " " + str(matrix_table[added_line][k])
        matrix_table.pop(added_line)
        table.content = matrix_table
    return True


def _merge_columns(table: MatrixTable, base_column: int, added_column: int) -> bool:
    if not table.abort():
        matrix_table = table.content
        for k in range(len(matrix_table)):
            if matrix_table[k][base_column] != matrix_table[k][added_column]:
                matrix_table[k][base_column] += " " + str(matrix_table[k][added_column])
            matrix_table[k].pop(added_column)
        table.content = matrix_table
    return True


def _detect_unit(table: MatrixTable, column_1: int, column_2: int) -> bool:
    """Because of how python-docx splits merged cells, two columns can have the same header, one of them containing the units associated to the other one."""
    if not table.abort():
        matrix_table = table.content
        rate_1, rate_2 = 0, 0
        for k in range(1, len(matrix_table)):
            if matrix_table[k][column_1] == matrix_table[k][column_2]:
                rate_1 += 1
                rate_2 += 1
                continue
            keep_going = False
            if matrix_table[k][column_1] in list_of_known_units:
                rate_1 += 1
                keep_going = True
            if matrix_table[k][column_2] in list_of_known_units:
                rate_2 += 1
                keep_going = True
            if not keep_going:
                break
        if rate_1 == len(matrix_table) - 1:
            return _merge_columns(
                table=table,
                base_column=column_2,
                added_column=column_1,
            )
        if rate_2 == len(matrix_table) - 1:
            return _merge_columns(
                table=table,
                base_column=column_1,
                added_column=column_2,
            )
    return False


def _correct_double(table: MatrixTable, column_1: int, column_2: int) -> bool:
    """A column header being repeated can be the result of a duplicated column.

    Handles the case where python-docx sometimes duplicates a column's content with another column's header.
    """
    if not table.abort():
        matrix_table = table.content
        similarities = [
            [0 for _ in range(len(matrix_table[0]))],
            [0 for _ in range(len(matrix_table[0]))],
        ]
        for k in range(1, len(matrix_table)):
            for m in range(len(matrix_table[k])):
                similarities[0][m] += matrix_table[k][m] == matrix_table[k][column_1]
                similarities[1][m] += matrix_table[k][m] == matrix_table[k][column_2]
        for k in range(len(similarities[0])):
            if k != column_1 and similarities[0][k] == len(matrix_table) - 1:
                for b in range(len(matrix_table)):
                    matrix_table[b].pop(column_1)
                table.content = matrix_table
                return True
            if k != column_2 and similarities[1][k] == len(matrix_table) - 1:
                for m in range(len(matrix_table)):
                    matrix_table[m].pop(column_2)
                table.content = matrix_table
                return True
    return abs(column_1 - column_2) == 1 and _merge_lines(
        table=table,
        base_line=0,
        added_line=1,
    )


def _unit_detection_loop(table: MatrixTable) -> MatrixTable:
    """First auxiliary function to make merge_first_line_doubles less complex."""
    units_done = False
    while not (table.abort() or units_done):
        matrix_table = table.content
        changed_something = False
        j = 1
        while not table.abort() and j < len(matrix_table[0]) - 1:
            increment = True
            if matrix_table[0][j] and matrix_table[0][j] == matrix_table[0][j + 1]:
                increment = not _detect_unit(table=table, column_1=j, column_2=j + 1)
                changed_something = (not increment) or changed_something
            matrix_table = table.content
            if increment:
                j += 1
        units_done = not changed_something
    return table


def _double_correction_loop(table: MatrixTable) -> tuple[MatrixTable, bool]:
    """Second auxiliary function to make merge_first_line_doubles less complex."""
    matrix_table = table.content
    changed_something = False
    j = 1
    while not table.abort() and j < len(matrix_table[0]):
        increment = True
        if matrix_table[0][j]:
            for k in range(j):
                if matrix_table[0][k] == matrix_table[0][j]:
                    changed_something = _correct_double(
                        table=table,
                        column_1=j,
                        column_2=k,
                    )
                    increment = not changed_something
                    if changed_something:
                        break
            matrix_table = table.content
        if increment:
            j += 1
    return table, changed_something


def _merge_first_line_doubles(table: MatrixTable) -> bool:
    """A column header being repeated can also be caused by the first line having been splitted on multiple lines.

    This function merges lines/columns according to the situation until no repetition remains on the first line.
    """
    table = _unit_detection_loop(table)
    first_line_done = False
    while not (table.abort() or first_line_done):
        table, changed_something = _double_correction_loop(table)
        first_line_done = not changed_something
    return True


def _merge_fake_lines(table: MatrixTable) -> bool:
    """Lines are sometimes splitted on multiple lines, which can cause sub-lines to not have a header.

    This function merges lines that do not have a header to the previous line.
    """
    if not table.abort():
        matrix_table = table.content
        i = 1
        while not table.abort() and i < len(matrix_table):
            increment = True
            if not matrix_table[i][0]:
                _merge_lines(table=table, base_line=i - 1, added_line=i)
                increment = False
            matrix_table = table.content
            if increment:
                i += 1
    return True


def _find_fake_columns(
    matrix_table: list[list[str]],
    i: int,
    open_symbol: bool,
    merge_left: bool,
    fake_column: bool,
) -> tuple[bool, bool, bool]:
    """Identifies if a column without a header must be merged to the left or to the right."""
    for k in range(1, len(matrix_table)):
        if matrix_table[k][i] not in list_of_known_units:
            if matrix_table[k][i] == matrix_table[k][i - 1]:
                merge_left = True
            elif i < len(matrix_table[0]) - 1 and (
                matrix_table[k][i] == matrix_table[k][i + 1]
            ):
                merge_left = False
            else:
                fake_column = False
                break
        else:
            open_symbol = open_symbol or (matrix_table[k][i] in {"(", "[", "{"})
            merge_left = (
                merge_left
                and (not open_symbol)
                and (
                    len(matrix_table[k][i - 1].replace(" ", "")) > 0
                    and matrix_table[k][i - 1].replace(" ", "")[-1]
                    not in list_of_known_units
                )
            )
            if not (merge_left or open_symbol):
                merge_left = merge_left or (
                    i < len(matrix_table[0]) - 1
                    and (
                        len(matrix_table[k][i + 1].replace(" ", "")) > 0
                        and matrix_table[k][i + 1].replace(" ", "")[-1]
                        in list_of_known_units
                    )
                )
    return open_symbol, merge_left, fake_column


def _merge_fake_columns(table: MatrixTable) -> bool:
    """Identifies columns that do not have a header or are units columns and merges them to the left/right according to the situation."""
    if not table.abort():
        matrix_table = table.content
        default_merge_left = True
        i = 1
        while not table.abort() and i < len(matrix_table[0]):
            increment = True
            if matrix_table[0][i] in list_of_known_units:
                fake_column = True
                default_merge_left = default_merge_left and i > 1
                merge_left = default_merge_left
                open_symbol = False

                open_symbol, merge_left, fake_column = _find_fake_columns(
                    matrix_table=matrix_table,
                    i=i,
                    open_symbol=open_symbol,
                    merge_left=merge_left,
                    fake_column=fake_column,
                )

                if fake_column:
                    increment = False
                    if merge_left or i == len(matrix_table[0]) - 1:
                        _merge_columns(table=table, base_column=i - 1, added_column=i)
                    elif open_symbol:
                        _merge_columns(table=table, base_column=i, added_column=i + 1)
                    else:
                        _merge_columns(table=table, base_column=i + 1, added_column=i)

            matrix_table = table.content
            if increment:
                i += 1
    return True


def compact_matrix(
    table: MatrixTable,
    do_check_if_splitted_cell: bool = True,
    do_square_format: bool = True,
    do_delete_empty_lines: bool = True,
    do_delete_empty_columns: bool = True,
    do_extract_title: bool = True,
    do_merge_first_line_doubles: bool = True,
    do_merge_fake_lines: bool = True,
    do_merge_fake_columns: bool = True,
) -> MatrixTable:
    """Global table processing functions, calling all the optional subtasks according to the situation.

    All subtasks used for correction of DOCX tables.
    Only a few used for other formats.
    Reasoning behind some functions explained in their respective docstrings.

    Args:
        table: MatrixTable object to process.
        do_check_if_splitted_cell: Boolean marker indicating whether or not to check if the table is a splitted XLSX cell.
        do_square_format: Boolean marker indicating whether or not to add cells to make sure the table is a rectangle (same number of cells for each line/column).
        do_delete_empty_lines: Boolean marker indicating whether or not to delete all empty lines.
        do_delete_empty_columns: Boolean marker indicating whether or not to delete all empty columns.
        do_extract_title: Boolean marker indicating whether or not to try to extract a title from the first line doubles in the table.
        do_merge_first_line_doubles: Boolean marker indicating whether or not to merge lines/columns until there are no doubles on the first line.
        do_merge_fake_lines: Boolean marker indicating whether or not to merge lines that were wrongfully separated.
        do_merge_fake_columns: Boolean marker indicating whether or not to merge columns that only contain units to adjacent columns.

    Returns:
        The corrected MatrixTable object.
    """
    if not table.abort() and do_check_if_splitted_cell:
        _check_if_splitted_cell(table)

    if not table.abort() and do_square_format:
        _square_format(table)

    if not table.abort() and do_delete_empty_lines:
        _delete_empty_lines(table)
    if not table.abort() and do_delete_empty_columns:
        _delete_empty_columns(table)

    if not table.abort() and do_extract_title:
        _extract_title(table)

    if not table.abort() and do_merge_first_line_doubles:
        _merge_first_line_doubles(table)

    if not table.abort() and do_merge_fake_lines:
        _merge_fake_lines(table)
    if not table.abort() and do_merge_fake_columns:
        _merge_fake_columns(table)

    return table
