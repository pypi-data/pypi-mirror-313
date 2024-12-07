import base64

from typing import List, Union

from antimatter_api import (
    AWSServiceAccountKeyInfo,
    GCPServiceAccountKeyInfo,
    AntimatterDelegatedAWSKeyInfo,
    KeyInfosKeyInformation,
    KeyInfos,
    AzureServiceAccountKeyInfo,
    AntimatterDelegatedAzureKeyInfo,
    BYOKKeyInfo,
)


class OverrideKeyInfosKeyInformation(KeyInfosKeyInformation):
    one_of_schemas: List[str] = [
        "AWSServiceAccountKeyInfo",
        "AntimatterDelegatedAWSKeyInfo",
        "GCPServiceAccountKeyInfo",
    ]


def aws_service_account_key_info(access_key_id: str, secret_access_key: str, key_arn: str = "") -> KeyInfos:
    """
    Create a KeyInfos object with AWS service account key information

    Example usage:

    .. code-block:: python

        key_info = aws_service_account_key_info(
            access_key_id="access_key_id", secret_access_key="secret_access_key", key_arn="key_arn"
        )

    :param access_key_id: The access key ID
    :param secret_access_key: The secret access key
    :param key_arn: The key ARN

    :return: A KeyInfos object with the specified key information
    """
    return KeyInfos(
        keyInformation=OverrideKeyInfosKeyInformation(
            actual_instance=AWSServiceAccountKeyInfo(
                access_key_id=access_key_id,
                secret_access_key=secret_access_key,
                key_arn=key_arn,
                provider_name="aws_sa",
            )
        )
    )


def antimatter_delegated_aws_key_info(key_arn: str) -> KeyInfos:
    """
    Create a KeyInfos object with Antimatter delegated AWS key information

    Example usage:

    .. code-block:: python

        key_info = antimatter_delegated_aws_key_info(key_arn="key_arn")

    :param key_arn: The key ARN

    :return: A KeyInfos object with the specified key information
    """
    return KeyInfos(
        keyInformation=OverrideKeyInfosKeyInformation(
            actual_instance=AntimatterDelegatedAWSKeyInfo(key_arn=key_arn, provider_name="aws_am"),
        )
    )


def gcp_service_account_key_info(
    project_id: str,
    location: str,
    key_ring_id: str = "",
    key_id: str = "",
    service_account_credentials: str = "",
    service_account_credentials_path: str = "",
) -> KeyInfos:
    """
    Create a KeyInfos object with GCP service account key information

    Example usage:

    .. code-block:: python

        key_info = gcp_service_account_key_info(
            project_id="project_id",
            location="location",
            key_ring_id="key_ring_id",
            key_id="key_id",
            service_account_credentials="<service_account_credentials_as_json_string>",
            service_account_credentials_path="/path/to/service_account_credentials.json"
        )

    Either `service_account_credentials` or `service_account_credentials_path` should be provided.

    :param project_id: The project ID
    :param location: The location
    :param key_ring_id: The key ring ID
    :param key_id: The key ID
    :param service_account_credentials: The service account credentials as JSON string
    :param service_account_credentials_path: The path to the service account credentials

    :return: A KeyInfos object with the specified key information
    """
    if not service_account_credentials and not service_account_credentials_path:
        raise ValueError(
            "Either service_account_credentials or service_account_credentials_path should be provided"
        )

    if service_account_credentials and service_account_credentials_path:
        raise ValueError(
            "Only one of service_account_credentials or service_account_credentials_path should be provided"
        )

    encoded_service_account_credentials = None
    if service_account_credentials_path:
        with open(service_account_credentials_path, "r") as f:
            encoded_service_account_credentials = base64.b64encode(f.read().encode()).decode("utf-8")

    if service_account_credentials:
        encoded_service_account_credentials = base64.b64encode(service_account_credentials.encode()).decode(
            "utf-8"
        )

    return KeyInfos(
        keyInformation=OverrideKeyInfosKeyInformation(
            actual_instance=GCPServiceAccountKeyInfo(
                service_account_credentials=encoded_service_account_credentials,
                project_id=project_id,
                location=location,
                keyring_id=key_ring_id,
                key_id=key_id,
                provider_name="gcp_sa",
            )
        )
    )


def azure_service_account_key_info(
    tenant_id: str,
    key_url: str,
    client_id: str,
    client_secret: str,
):
    """
    Create a KeyInfos object with Azure service account key information

    Example usage:

    .. code-block:: python

        key_info = azure_service_account_key_info(
            tenant_id="tenant_id",
            key_url="key_url",
            client_id="client_id",
            client_secret="client_secret",
        )

    :param tenant_id: The Azure service account directory ID
    :param key_url: The name of the key in Azure HSM
    :param client_id: The access key ID's secret access key
    :param client_secret: The access key ID's secret access key
    """

    return KeyInfos(
        keyInformation=OverrideKeyInfosKeyInformation(
            actual_instance=AzureServiceAccountKeyInfo(
                tenant_id=tenant_id,
                key_url=key_url,
                client_id=client_id,
                client_secret=client_secret,
                provider_name="azure_sa",
            )
        )
    )


def antimatter_delegated_azure_key_info(
    tenant_id: str,
    key_url: str,
):
    """
    Create a KeyInfos object with Azure HSM root encryption key information that has been delegated to Antimatter's Azure account

    Example usage:

    .. code-block:: python

        key_info = antimatter_delegated_azure_key_info(
            tenant_id="tenant_id",
            key_url="key_url",
        )

    :param tenant_id: The directory ID in containing the managed HSM
    :param key_url: The full URL for the key
    """

    return KeyInfos(
        keyInformation=OverrideKeyInfosKeyInformation(
            actual_instance=AntimatterDelegatedAzureKeyInfo(
                tenant_id=tenant_id,
                key_url=key_url,
                provider_name="azure_am",
            )
        )
    )


def byok_key_info(
    key: Union[bytes, str],
):
    """
    Create a BYOK key info object with the specified key information

    Example usage:

    .. code-block:: python

        key_info = byok_key_info(
            key="key"
        )

    :param key: The base64-encoded key material to use as the basis for an encryption key. It must be 256 bytes or longer

    :return: A BYOKKeyInfo object with the specified key information
    """

    return KeyInfos(
        keyInformation=OverrideKeyInfosKeyInformation(
            actual_instance=BYOKKeyInfo(
                key=key,
                provider_name="byok",
            )
        )
    )
