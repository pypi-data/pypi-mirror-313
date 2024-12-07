import re

_cell_path_pattern = re.compile(r"(.*)\[(\d+)]$")


def cell_path(cname: str, rnum: int):
    """
    Helper function to get a cell path name from a column name and row number.
    This can be used for a manual SpanTag

    :param cname: The column name of the cell
    :param rnum: The row number of the cell
    :return: The name of the cell path
    """
    return f"{cname}[{rnum}]"


def col_name(path: str) -> str:
    """
    Extract the column name from a cell path

    :param path: The name of the cell path
    :return: The column name of the cell
    """
    if m := _cell_path_pattern.match(path):
        return m.group(1)
    return ""


def row_num(path: str) -> int:
    """
    Extract the row number from a cell path

    :param path: The name of the cell path
    :return: The row number of the cell
    """
    if m := _cell_path_pattern.match(path):
        return int(m.group(2))
    return -1
