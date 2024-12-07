import re
from typing import Any, Dict, List, Tuple

# For type hinting
try:
    import pandas as pd
except ModuleNotFoundError:
    pass

import antimatter.extra_helper as extra_helper
from antimatter.errors import DataFormatError, MissingDependency
from antimatter.fieldtype.infer import infer_fieldtype
from antimatter.handlers.base import DataHandler


class PandasDataFrame(DataHandler):
    """
    The PandasDataFrame DataHandler supports a pandas DataFrame. There are
    some restrictions on the underlying dataset which must be a two-dimensional
    data set, or a list of two-dimensional data sets.
    """

    def from_generic(self, cols: List[str], generic_data: List[List[bytes]], extra: Dict[str, Any]) -> Any:
        """
        from_generic loads the generic data into a pandas DataFrame, passing any
        extra parameters transparently to the DataFrame constructor.

        :param cols: the column names for the underlying data
        :param generic_data: the data rows that are loaded into a pandas DataFrame
        :param extra: extra data for the DataHandler, passed into the pandas DataFrame
        :return: the pandas DataFrame built with the dataset
        """
        try:
            import pandas as pd
        except ModuleNotFoundError as me:
            raise MissingDependency(me)

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

        df = pd.DataFrame(
            data=data,
            columns=cols,  # or None,
            **extra_helper.without_meta(extra),
        )

        # update columns with persisted dtypes
        for cname, dtype in extra.get(extra_helper.DTYPE_KEY, {}).items():
            try:
                df[cname] = df[cname].astype(dtype)
            except NotImplementedError:
                # pyarrow.decimal128 doesn't support dtype handling by name
                if m := re.match(r"decimal128\((\d+), ?(\d+)\)\[pyarrow]", dtype):
                    try:
                        import pyarrow
                    except ModuleNotFoundError as me:
                        raise MissingDependency(me)
                    df[cname] = df[cname].astype(
                        pd.ArrowDtype(pyarrow.decimal128(int(m.group(1)), int(m.group(2))))
                    )
                else:
                    raise

        return df

    def to_generic(self, df: Any) -> Tuple[List[str], List[List[bytes]], Dict[str, Any]]:
        """
        to_generic converts a pandas DataFrame into the generic data format,
        formatting the underlying data based on if the underlying data set is
        a list of two-dimensional records or a single two-dimensional record.

        :param df: the DataFrame to extract generic format data from the underlying data set
        :return: the data in its generic form
        """
        try:
            import pandas as pd
        except ModuleNotFoundError as me:
            raise MissingDependency(me)

        rows = []
        extra = {}
        cols = df.columns.tolist()
        col_ft_cache = {}

        if self._data_is_not_2d(df):
            raise DataFormatError("only 2-dimensional DataFrames are supported")

        data = df.to_dict(orient="records")

        # Get dtypes for each column
        if data:
            extra[extra_helper.COL_TYPE_KEY] = {}

            # persist dtypes (where not generic 'object')
            dtypes = {}
            for cname in cols:
                dtype = df[cname].dtype
                if dtype.name != "object":
                    dtypes[str(cname)] = dtype.name
            extra[extra_helper.DTYPE_KEY] = dtypes

        # Flatten data into rows
        for d in data:
            row = []
            for cname in cols:
                val = d[cname]
                ft = col_ft_cache.get(cname)
                if ft is None:
                    ft = infer_fieldtype(val)
                    extra[extra_helper.COL_TYPE_KEY][str(cname)] = ft.value
                    col_ft_cache[cname] = ft
                val = self.field_converter_to_generic(ft)(val)
                row.append(val)
            rows.append(row)

        return [str(c) for c in cols], rows, extra

    @staticmethod
    def _data_is_not_2d(df: Any) -> bool:
        """
        Determine if the data is not 2-dimensional by inspecting the contents
        of the first column.

        :param df: The DataFrame to examine
        :return: If the data not 2-dimensional
        """
        c = df.columns
        if len(c) < 1:
            return False
        cvals = df[c[0]]
        if len(cvals) < 1:
            return False
        return isinstance(cvals[0], list)
