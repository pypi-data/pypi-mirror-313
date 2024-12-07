from typing import Any, Dict, List, Tuple

from antimatter.errors import MissingDependency

# For type hinting
try:
    from torch.utils.data import DataLoader, Dataset
except ModuleNotFoundError:
    pass

import antimatter.extra_helper as extra_helper
from antimatter import errors
from antimatter.fieldtype.infer import infer_fieldtype
from antimatter.handlers.base import DataHandler


class PytorchDataLoader(DataHandler):
    """
    The PytorchDataLoader DataHandler supports a pytorch DataLoader. There are
    some restrictions on the underlying dataset, which must be iterable, producing
    two-dimensional dictionaries.
    """

    def from_generic(self, cols: List[str], generic_data: List[List[bytes]], extra: Dict[str, Any]) -> Any:
        """
        from_generic loads the generic data as a dataset into the pytorch
        DataLoader, passing any extra parameters transparently to the DataLoader
        constructor

        :param cols: the column names for the underlying data
        :param generic_data: the capsule's generic data format that is loaded into a pytorch DataLoader
        :param extra: extra data for the DataHandler, passed into the pytorch DataLoader constructor
        :return: the pytorch DataLoader built with the dataset
        """
        try:
            from torch.utils.data import DataLoader, Dataset
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

        # TODO: Should we support user-passed DataSets? Tensors?
        dl = DataLoader(PytorchDataLoader.PytorchDataLoaderDataSet(data), **extra_helper.without_meta(extra))
        return dl

    def to_generic(self, dl: Any) -> Tuple[List[str], List[List[bytes]], Dict[str, Any]]:
        """
        to_generic converts a pytorch DataLoader into the generic data format,
        iterating through the DataLoader's data set, expecting each iterated
        item to be a 2-dimensional dictionary.

        :param dl: the DataLoader to extract generic format data from
        :return: the data in its generic form
        """
        try:
            from torch.utils.data import DataLoader
        except ModuleNotFoundError as me:
            raise MissingDependency(me)

        cols = set()
        data = []

        # First pass: get column names, validate data shape/format, and build
        # intermediate dictionaries
        for e in dl.dataset:
            try:
                # TODO: Don't need to be this restrictive? Can support more formats
                d = dict(e)
                cols.update(set(d.keys()))
                data.append(d)
            except ValueError:
                raise errors.DataFormatError(
                    "only 2-dimensional DataSets that can be cast to dictionary are supported"
                )

        # Second pass: flatten dicts into rows
        rows = []
        extra = {}
        cols = list(cols)
        col_ft_cache = {}
        if data:
            extra[extra_helper.COL_TYPE_KEY] = {}
        for d in data:
            row = []
            for cname in cols:
                # TODO: Handle 'missing' values using 'extras' dict
                val = d.get(cname, "")
                ft = col_ft_cache.get(cname)
                if ft is None:
                    ft = infer_fieldtype(val)
                    extra[extra_helper.COL_TYPE_KEY][str(cname)] = ft.value
                    col_ft_cache[cname] = ft
                val = self.field_converter_to_generic(ft)(val)
                row.append(val)
            rows.append(row)

        # TODO: Should extract more potential arguments for the constructor
        return [str(c) for c in cols], rows, {**extra, "batch_size": dl.batch_size}

    try:

        class PytorchDataLoaderDataSet(Dataset):
            """
            The PytorchDataLoaderDataSet extends the pytorch Dataset to wrap the
            underlying data to support particular properties required of a DataLoader's
            Dataset.
            """

            def __init__(self, generic_data: List[Dict[str, Any]]):
                """
                Wraps generically formatted Capsule data in a pytorch Dataset.

                :param generic_data: the capsule's generic data format
                """
                self.data = generic_data

            def __len__(self):
                """Gets the length of the dataset"""
                return len(self.data)

            def __getitem__(self, idx):
                """Gets the item in the data set at the given index"""
                return self.data[idx]

            def __eq__(self, other):
                """Checks this dataset with another dataset for equality"""
                if len(self) != len(other):
                    return False

                for i, v in enumerate(self.data):
                    if not v == other[i]:
                        return False

                return True

    except (ModuleNotFoundError, NameError):
        # If we hit this point, the pytorch dependencies have not been imported yet.
        # We only want to fail or warn if the caller attempts to use pytorch, so
        # swallow the error for now
        pass
