import abc
from typing import Any, Callable, Dict, List, Tuple

from antimatter import errors
from antimatter.fieldtype import converters
from antimatter.fieldtype.fieldtypes import FieldType


class DataHandler(abc.ABC):
    """
    Abstract base DataHandler defining the supporting methods a handler for a
    Datatype must implement. A Datatype must support converting from its native
    type to the generic internal format and back. This conversion should be
    lossless so that the data added to a Capsule will behave the same when
    loaded back out.
    """

    @abc.abstractmethod
    def from_generic(self, cols: List[str], generic_data: List[List[bytes]], extra: Dict[str, Any]) -> Any:
        """
        from_generic takes data in its generic form, with a list of column
        names and a list of data rows, and converts it into the handler's
        specific data type.

        :param cols: list of column names for the data
        :param generic_data: list of dictionaries of data
        :param extra: extra information for the handler use when processing
        :return: the data in the handler's specific data format
        """
        pass

    @abc.abstractmethod
    def to_generic(self, data: Any) -> Tuple[List[str], List[List[bytes]], Dict[str, Any]]:
        """
        to_generic converts data from the handler's specific data type into a
        generic form of a list of column names (if applicable), a list of data
        rows, and a dictionary containing any extra processing info.

        :param data: the data in the handler's specific data format
        :return: the data in its generic form
        """
        pass

    def field_converter_from_generic(self, ft: FieldType) -> Callable[[bytes], Any]:
        """
        field_converter_from_generic gets a field converter function for the
        given field type that can be used to convert fields from their generic
        string type to their specific type.

        Note that these statement should be true for all implementations, given
        FieldType ft.

        from_gen = field_converter_from_generic(ft)
        to_gen = field_converter_to_generic(ft)

        generic_value == to_gen(from_gen(generic_value))
        field_value == from_gen(to_gen(field_value))

        :param ft: the FieldType to get the converter function for
        :return: a function that can convert field values from generic form
        """
        if (conv := converters.Standard.field_converter_from_generic(ft)) is None:
            raise errors.DataFormatError(f"DataHandler does not support fieldtype {ft} from generic")
        return conv

    def field_converter_to_generic(self, ft: FieldType) -> Callable[[Any], bytes]:
        """
        field_converter_to_generic gets a field converter function for the given
        field type that can be used to convert fields from their specific type
        to their generic type.

        Note that these statement should be true for all implementations, given
        FieldType ft.

        from_gen = field_converter_from_generic(ft)
        to_gen = field_converter_to_generic(ft)

        generic_value == to_gen(from_gen(generic_value))
        field_value == from_gen(to_gen(field_value))

        :param ft: the FieldType to get the converter function for
        :return: a function that can convert field values to generic form
        """
        if (conv := converters.Standard.field_converter_to_generic(ft)) is None:
            raise errors.DataFormatError(f"DataHandler does not support fieldtype {ft} to generic")
        return conv
