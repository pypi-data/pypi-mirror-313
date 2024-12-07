import itertools

import pytest

from antimatter.datatype.datatypes import Datatype
from antimatter.fieldtype.fieldtypes import FieldType
from antimatter.handlers import factory

datatypes = [dt for dt in Datatype if dt is not Datatype.Unknown]
fieldtypes = [ft for ft in FieldType]
dt_ft_pairs = list(itertools.product(datatypes, fieldtypes))


class TestFieldTypes:
    """
    TestFieldTypes is a safeguard test to ensure that every FieldType is handled
    by each handler.
    """

    @pytest.mark.parametrize(
        ("datatype", "fieldtype"),
        dt_ft_pairs,
        ids=[f"{dt.value} Datatype with FieldType {ft.value}" for dt, ft in dt_ft_pairs],
    )
    def test_handler_implementations_to_generic(self, datatype: Datatype, fieldtype: FieldType):
        handler = factory(datatype)
        assert handler.field_converter_to_generic(fieldtype) is not None

    @pytest.mark.parametrize(
        ("datatype", "fieldtype"),
        dt_ft_pairs,
        ids=[f"{dt.value} Datatype with FieldType {ft.value}" for dt, ft in dt_ft_pairs],
    )
    def test_handler_implementations_from_generic(self, datatype: Datatype, fieldtype: FieldType):
        handler = factory(datatype)
        assert handler.field_converter_from_generic(fieldtype) is not None
