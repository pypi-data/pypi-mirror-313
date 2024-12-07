from typing import Any, Dict, List, Tuple

import antimatter.extra_helper as extra_helper
from antimatter.extra_helper import COL_TYPE_KEY
from antimatter.fieldtype.infer import infer_fieldtype
from antimatter.handlers.base import DataHandler


class Dictionary(DataHandler):
    """
    The Dictionary DataHandler supports a single dictionary value with string
    keys.
    """

    def from_generic(self, cols: List[str], generic_data: List[List[bytes]], extra: dict) -> Dict[str, Any]:
        """
        from_generic expects at most one dictionary in the generic data list,
        and extracts and flattens this dictionary if it can be found

        :param cols: the column names; should be the string key values in the dictionary
        :param generic_data: the capsule's generic data format holding the values of the single row
        :param extra: extra data for the DataHandler
        :return: the dictionary value held in the generic data format
        """
        if generic_data:
            data = {}
            for col, field in zip(cols, generic_data[0]):
                ft = extra_helper.get_field_type(col, extra)
                data[col] = self.field_converter_from_generic(ft)(field)
            return data
        return {}

    def to_generic(self, data: Dict[str, Any]) -> Tuple[List[str], List[List[bytes]], Dict[str, Any]]:
        """
        to_generic converts a single dictionary value into the generic data
        format, flattening the dictionary into a list and extracting the keys
        in the key:value pairs as the column names.

        :param data: the dictionary value to wrap into a generic format
        :return: the data in its generic form
        """
        cols = []
        row = []
        extra = {}
        if data:
            extra[COL_TYPE_KEY] = {}
        for cname, val in data.items():
            cols.append(cname)
            ft = infer_fieldtype(val)
            field = self.field_converter_to_generic(ft)(val)
            row.append(field)
            extra[COL_TYPE_KEY][cname] = ft.value
        return cols, [row], extra
