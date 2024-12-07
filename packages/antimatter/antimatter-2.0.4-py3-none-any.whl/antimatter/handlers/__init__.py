from antimatter.datatype.datatypes import Datatype
from antimatter.errors import HandlerFactoryError
from antimatter.handlers.base import DataHandler
from antimatter.handlers.dict_list import DictList
from antimatter.handlers.dictionary import Dictionary
from antimatter.handlers.langchain import LangchainHandler
from antimatter.handlers.pandas_dataframe import PandasDataFrame
from antimatter.handlers.pytorch_dataloader import PytorchDataLoader
from antimatter.handlers.scalar import ScalarHandler


def factory(datatype: Datatype) -> DataHandler:
    """
    Factory returns an instance of a DataHandler matching the provided Datatype.

    :param datatype: The Datatype to get a handler for.
    :return:
        An implementation of the abstract DataHandler for handling data of the
        given type.
    """
    if datatype is Datatype.Unknown:
        raise HandlerFactoryError("cannot create factory from 'Unknown' Datatype")
    elif datatype is Datatype.Scalar:
        return ScalarHandler()
    elif datatype is Datatype.Dict:
        return Dictionary()
    elif datatype is Datatype.DictList:
        return DictList()
    elif datatype is Datatype.PandasDataframe:
        return PandasDataFrame()
    elif datatype is Datatype.PytorchDataLoader:
        return PytorchDataLoader()
    elif datatype is Datatype.LangchainRetriever:
        return LangchainHandler()
    else:
        raise HandlerFactoryError(f"no handler found for Datatype: {datatype}")
