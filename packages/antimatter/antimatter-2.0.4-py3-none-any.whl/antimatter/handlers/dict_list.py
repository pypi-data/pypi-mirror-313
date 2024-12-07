from typing import Any, Dict, List, Tuple

import antimatter.extra_helper as extra_helper
from antimatter.extra_helper import COL_TYPE_KEY
from antimatter.fieldtype.infer import infer_fieldtype
from antimatter.handlers.base import DataHandler


class DictList(DataHandler):
    """The DictList DataHandler supports a list of dictionaries."""

    def from_generic(
        self, cols: List[str], generic_data: List[List[bytes]], extra: dict
    ) -> List[Dict[str, Any]]:
        """
        from_generic takes the generic data and passes it on as a list of
        dictionaries

        :param cols: the column names
        :param generic_data:
            the capsule's generic data format holding the row values
        :param extra: extra data for the DataHandler
        :return: the data in a dictionary list format
        """
        col_ft_cache = {}

        data = []
        for generic_row in generic_data:
            row = {}
            for col, field in zip(cols, generic_row):
                ft = col_ft_cache.get(col)
                if ft is None:
                    ft = extra_helper.get_field_type(col, extra)
                col_ft_cache[col] = ft
                row[col] = self.field_converter_from_generic(ft)(field)
            data.append(row)
        return data

    def to_generic(self, data: List[Dict[str, Any]]) -> Tuple[List[str], List[List[bytes]], Dict[str, Any]]:
        """
        to_generic converts a list of dictionaries into the generic data format,
        which is essentially a no-op as DictList has the same format as generic

        :param data: the list of dictionaries to pass across as generic format
        :return: the data in its generic form
        """
        cols = set()
        rows = []
        extra = {}

        col_ft_cache = {}
        if data:
            extra[COL_TYPE_KEY] = {}

        # First pass: get column names
        [cols.add(key) for d in data for key in d]

        # Second pass: flatten dicts into rows
        cols = list(cols)
        for d in data:
            row = []
            for cname in cols:
                # TODO: Handle 'missing' values using 'extras' dict
                val = d.get(cname)
                if val is None:
                    val = ""
                else:
                    ft = col_ft_cache.get(cname)
                    if ft is None:
                        ft = infer_fieldtype(val)
                    extra[COL_TYPE_KEY][cname] = ft.value
                    col_ft_cache[cname] = ft
                    val = self.field_converter_to_generic(ft)(val)
                row.append(val)
            rows.append(row)

        return cols, rows, extra
