from typing import Any, Dict, Optional

import antimatter_api as openapi_client


def serialize_identity_provider_info_dict(model: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Serialize an identity provider info dictionary

    :param model: The identity provider info dictionary
    :return: The serialized dictionary
    """
    if model is None:
        return None
    return {k: v for k, v in model.items()}


def serialize_identity_principal_details_dict(model: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Serialize an identity principal details dictionary

    :param model: The identity principal details dictionary
    :return: The serialized dictionary
    """
    if model is None:
        return None
    return {k: v for k, v in model.items()}


def deserialize_identity_principal_details_json_str(model: Optional[str]) -> openapi_client.PrincipalInfo:
    """
    Deserialize an identity principal details json string into a PrincipalInfo object

    :param model: The identity principal details JSON string
    :return: The PrincipalInfo object
    """
    if model is None:
        return None

    return openapi_client.PrincipalInfo.from_json(model)
