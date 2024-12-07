from typing import Any, Dict, List, Tuple

import antimatter.extra_helper as extra_helper
from antimatter.extra_helper import COL_TYPE_KEY, DEFAULT_COL_NAME
from antimatter.fieldtype.infer import infer_fieldtype
from antimatter.handlers.base import DataHandler


class ScalarHandler(DataHandler):
    """
    The Scalar DataHandler supports a scalar value.
    """

    def from_generic(self, cols: List[str], generic_data: List[List[bytes]], extra: Dict[str, Any]) -> Any:
        """
        from_generic expects a single value in a list of lists and extracts
        this value if it can be found.

        :param cols: ignored when converting from generic as the column is a static name.
        :param generic_data: the generic data holder wrapping a single value.
        :param extra: extra data for the DataHandler. Ignored when converting.
        :return: the value held in the generic data format
        """
        if generic_data and generic_data[0] and cols:
            field = generic_data[0][0]
            ft = extra_helper.get_field_type(cols[0], extra)
            return self.field_converter_from_generic(ft)(field)
        return ""

    def to_generic(self, data: Any) -> Tuple[list, List[List[bytes]], Dict[str, Any]]:
        """
        to_generic converts a scalar value into the generic data format.

        :param data: the scalar value to wrap into a generic format
        :return: the data in its generic form
        """
        ft = infer_fieldtype(data)
        field = self.field_converter_to_generic(ft)(data)
        return [DEFAULT_COL_NAME], [[field]], {COL_TYPE_KEY: {DEFAULT_COL_NAME: ft.value}}
