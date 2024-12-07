from typing import Any

from antimatter import errors
from antimatter.datatype.datatypes import Datatype
from antimatter.fieldtype.infer import infer_fieldtype

DICT_LIST_FMT_ERROR = "data in a list format must contain dictionaries"


def infer_datatype(data: Any) -> Datatype:
    """
    Convenience handler for inferring the Datatype from an instance of a data
    object. Supported data types include string value, dictionary, list of
    dictionaries, pandas DataFrame, pytorch DataLoader, and langchain Retriever

    :param data: Instance of a data object to get the Datatype for.
    :return: The Datatype whose handler can work with the provided data instance.
    """
    if isinstance(data, dict):
        return Datatype.Dict

    if isinstance(data, list):
        if all([isinstance(x, dict) for x in data]):
            return Datatype.DictList
        else:
            raise TypeError(DICT_LIST_FMT_ERROR)

    try:
        import pandas as pd

        if isinstance(data, pd.DataFrame):
            return Datatype.PandasDataframe
    except ModuleNotFoundError:
        pass

    try:
        from torch.utils.data import DataLoader

        if isinstance(data, DataLoader):
            return Datatype.PytorchDataLoader
    except ModuleNotFoundError:
        pass

    try:
        from langchain.schema.retriever import BaseRetriever

        if isinstance(data, BaseRetriever):
            return Datatype.LangchainRetriever
    except ModuleNotFoundError:
        pass

    try:
        # Use `infer_fieldtype` to check if it's a supported scalar value by
        # inferring the FieldType. If not inferred, DataFormatError is raised.
        infer_fieldtype(data)
        return Datatype.Scalar
    except errors.DataFormatError:
        return Datatype.Unknown
