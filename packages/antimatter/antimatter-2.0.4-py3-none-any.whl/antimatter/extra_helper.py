import json
from typing import Any, Dict, List, Optional

from antimatter.datatype.datatypes import Datatype
from antimatter.fieldtype.fieldtypes import FieldType

META_TYPE_KEY = "_metadtype"
COL_TYPE_KEY = "_coltype"
DTYPE_KEY = "_dtype"

ALL_META_KEYS = [META_TYPE_KEY, COL_TYPE_KEY, DTYPE_KEY]

DEFAULT_COL_NAME = "content"


def extra_dict_from_string(
    serialized_extra: Optional[str],
    row_cnt: int = -1,
    col_names: List[str] = None,
) -> Dict[str, Any]:
    """
    Parses an 'extra' dictionary from a string. The string, if present, is
    expected to be a serialized JSON format dictionary.

    If 'extra' is empty or None, a default extra dict will be returned based on
    the row count and column names, following these rules for determining the
    default type when the 'extra' dictionary is not supplied:
    1. If it can be determined that the data is a scalar value by virtue of only
    one row and column of data existing with the default 'content' column name,
    the default type will be set as a Scalar value.
    2. Otherwise, if only one row exists, the default type will be set as a Dict.
    3. In all other cases, the default type will be set as a DictList.

    :param serialized_extra: The serialized 'extra' dictionary
    :param row_cnt: The number of rows in the data set
    :param col_names: The names of the columns in the data set
    :return: A parsed 'extra' dictionary
    """
    if col_names is None:
        col_names = []
    if not serialized_extra:
        if row_cnt == 1:
            if len(col_names) == 1 and col_names[0] == DEFAULT_COL_NAME:
                top_lvl_type = Datatype.Scalar.value
            else:
                top_lvl_type = Datatype.Dict.value
        else:
            top_lvl_type = Datatype.DictList.value
        return {top_lvl_type: {}, COL_TYPE_KEY: {}, META_TYPE_KEY: top_lvl_type}
    else:
        return json.loads(serialized_extra)


def extra_for_session(
    dt: Datatype,
    from_capsule: Dict[str, Any],
    session_extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Arranges an 'extra' dictionary for a Session using the given Datatype
    and the 'extra' dictionary built from a handler's "to_generic" method.
    If an existing session "extra" dictionary is provided, it will be
    updated with the additional information.

    :param dt: the Datatype for the capsule data
    :param from_capsule: the 'extra' data from the capsule level generic handling
    :param session_extra: an optional existing Session level 'extra' dict
    :return: a Session level 'extra' dict for passing metadata to a Capsule
    """
    if not session_extra:
        session_extra = {}
    if dt.value not in session_extra:
        session_extra[dt.value] = {}
    for meta_key in [COL_TYPE_KEY, DTYPE_KEY]:
        if meta_key in from_capsule:
            session_extra[meta_key] = from_capsule[meta_key]
    session_extra[dt.value].update(without_meta(from_capsule))
    session_extra[META_TYPE_KEY] = dt.value
    return session_extra


def extra_for_capsule(
    dt: Datatype,
    session_extra: Optional[Dict[str, Any]],
    **kwargs,
) -> Dict[str, Any]:
    """
    Arranges an 'extra' dictionary for a Capsule using the given Datatype to
    load the Capsule in and the Session level 'extra' dictionary. If kwargs are
    provided, they will be passed as-is to the 'extra' dictionary.

    :param dt: the Datatype for the Capsule data
    :param session_extra: the Session level 'extra' dict
    :param kwargs: the kwargs passed to a Capsule for reading data
    :return: a Capsule level 'extra' dict for passing metadata to a data handler
    """
    for_capsule = {**kwargs, **session_extra.get(dt.value, {})}
    for meta_key in ALL_META_KEYS:
        if meta_key in session_extra:
            for_capsule[meta_key] = session_extra[meta_key]
    return for_capsule


def get_field_type(
    col_name: str,
    extra: Optional[Dict[str, Any]],
    default: FieldType = FieldType.String,
) -> FieldType:
    """
    Helper function to get the field type from a Capsule level 'extra' dictionary
    for the provided column name, falling back to the default value.

    :param col_name: the name of the column to get the field type metadata for
    :param extra: the Capsule level 'extra' dict containing handler metadata
    :param default: fallback FieldType value (String by default)
    :return: the FieldType of the given column as found in the 'extra' metadata
    """
    if not extra:
        extra = {}
    ft_val = extra.get(COL_TYPE_KEY, {}).get(col_name, default)
    return FieldType(ft_val)


def without_meta(extra: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Helper function to strip special metadata keys from the provided 'extra'
    dictionary. A new copy of the dictionary is made and returned.

    :param extra: the 'extra' dict to strip special metadata from
    :return: the 'extra' dict with special metadata stripped
    """
    return {k: v for k, v in extra.items() if k not in ALL_META_KEYS}
