from antimatter.cell_utils import cell_path, col_name, row_num


def test_cell_path():
    cname = "column"
    rnum = 42
    expected = "column[42]"

    path = cell_path(cname, rnum)
    assert path == expected

    assert col_name(path) == cname
    assert row_num(path) == rnum
