import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union
from urllib.parse import quote_plus, urlparse


import antimatter_api as openapi_client
import antimatter.handlers as handlers
from antimatter.auth.config.auth_config import AuthConfig
from antimatter.authn import (
    ApiKeyAuthentication,
    Authentication,
    GoogleOAuthAuthentication,
    OAuthDomainAuthentication,
    StaticOAuthAuthentication,
    Unauthenticated,
)
from antimatter.authz import TokenAuthorization
from antimatter.cap_prep.prep import Preparer
from antimatter.capsule import Capsule, CapsuleBindings
from antimatter.datatype.datatypes import Datatype
from antimatter.datatype.infer import infer_datatype
from antimatter import errors
from antimatter.extra_helper import extra_for_session
from antimatter.filetype.extract import extract_from_file
from antimatter.filetype.infer import infer_filetype
from antimatter.session_mixins import (
    CapabilityMixin,
    CapsuleMixin,
    DomainMixin,
    EncryptionMixin,
    FactMixin,
    GeneralMixin,
    IdentityProviderMixin,
    PolicyRuleMixin,
    ReadContextMixin,
    RootEncryptionKeyMixin,
    StarredDomainMixin,
    VerificationMixin,
    WriteContextMixin,
    DataPolicyMixin,
)
from antimatter.tags import ColumnTag, RowTag, SpanTag


def new_domain(
    email: str,
    provider: str = None,
    display_name: Optional[str] = None,
    config_path: Optional[str] = None,
    add_to_config: bool = True,
    make_active: bool = False,
    enable_retries: bool = True,
) -> "Session":
    """
    Create a new domain with the provided email as the admin contact. A
    verification email will be sent to that email. Verification must be completed
    before the Antimatter API can be interacted with.
    If the provider is 'google', the session will be authenticated with a Google
    OAuth token. That domain will be added to the starred domains as well.

    :param email: The admin contact email used for email verification
    :param provider: The provider to use for authentication; default is None
    :param display_name: The display name for the new domain
    :param config_path: The path to the domain profile config file; default is ~/.antimatter/config
    :param add_to_config: Whether to add the new domain to the config file; default is True
    :param make_active: Whether to make the new domain the active profile in the config file; default is False
    :param enable_retries: If True, retry gateway, DNS, and general connection errors
    :return: A Session holding the newly created domain_id and api_key
    """
    # Try to create the Session before potentially adding to the config file - if creating
    # the Session produces an erroneous result, we don't want to add it to the config
    auth_conf = AuthConfig.from_file(config_path)

    authn = Unauthenticated(admin_email=email, enable_retries=enable_retries)
    session = Session(authn)
    session.new_domain(email, display_name=display_name, reauthenticate=True)

    if add_to_config or make_active:
        try:
            auth_conf.add_profile(
                domain_id=session.domain_id,
                api_key=session.api_key,
                name=display_name,
                mark_active=make_active,
                write_to_file=True,
            )
        except Exception as e:
            # Catch any failures as we don't want the caller to lose the domain ID and API key
            # if saving to a config file goes wrong
            print(f"error saving profile to config file: {e}", file=sys.stderr)

    if provider == "google":
        global_session = Session(GoogleOAuthAuthentication(enable_retries=enable_retries))
        global_session.add_starred_domain(session.domain_id)

    # Finally, return the Session
    return session


def load_domain(
    domain_id: Optional[str] = None,
    api_key: Optional[str] = None,
    provider: Optional[str] = None,
    idp: Optional[str] = None,
    display_name: Optional[str] = None,
    config_path: Optional[str] = None,
    add_to_config: bool = False,
    make_active: bool = False,
    enable_retries: bool = True,
) -> "Session":
    """
    Load an existing domain. There are several different ways to specify the domain
    credentials to use, from highest to lowest priority.

    1. Using display name. If this is present, it will attempt to load a profile
    from the config file with this name.
    2. Using domain_id and api_key as the credentials.
    3. Using domain_id and a provider. If this is present, it will attempt to load a profile
    using an oauth provider.
    4. Using only domain_id. If this is present, it will attempt to load a profile
    from the config file that matches this domain ID.

    If domain_id is not provided, this will check the ANTIMATTER_DOMAIN_ID env var
    for a domain ID.

    If api_key is not provided, this will check the ANTIMATTER_API_KEY env var for
    an API key.

    The config file is by default expected to exist at ~/.antimatter/config, but an
    override location can be provided with the config_path argument, or the
    ANTIMATTER_CONFIG_PATH env var.

    By default, loading an existing domain will not add the credentials to the profile
    auth config file. Set add_to_config to True to add this domain to the config. To
    make this domain the active profile, set make_active to True. Note that setting
    make_active to True implicitly sets add_to_config to True.

    :param domain_id: The domain ID of the domain to load
    :param api_key: The API key of the domain to load
    :param provider: The name of the oauth provider to use for authentication
    :param display_name: The display name in the auth config file of the domain to load
    :param config_path: The path to the domain profile config file; default is ~/.antimatter/config
    :param add_to_config: Whether to add the domain to the config file; default is False
    :param make_active: Whether to make the domain the active profile in the config file; default is False
    :param enable_retries: If True, retry gateway, DNS, and general connection errors
    :return: A Session holding the existing domain_id and api_key
    """
    if not domain_id:
        domain_id = os.getenv("ANTIMATTER_DOMAIN_ID", None)
    if not api_key:
        api_key = os.getenv("ANTIMATTER_API_KEY", None)
    if not config_path:
        config_path = os.getenv("ANTIMATTER_CONFIG_PATH", None)
    if not provider:
        provider = os.getenv("ANTIMATTER_OAUTH_PROVIDER", None)

    # If a domain and API key or provider are available, and no display name was specified, and no flags
    # have been set to save to the config file, skip loading the auth config profiles
    # because we won't use them
    if not display_name and domain_id and (api_key or provider) and not add_to_config and not make_active:
        auth_conf = AuthConfig()
    else:
        auth_conf = AuthConfig.from_file(config_path)

    name = None
    from_conf = False
    token = None

    # If a display name is specified, load that profile
    if display_name:
        pconf = auth_conf.get_profile(name=display_name)
        if pconf is None:
            raise errors.SessionLoadError(f"could not find profile {display_name} in profile config")
        name = pconf.name
        domain_id = pconf.domain_id
        api_key = pconf.api_key
        from_conf = True
        token = pconf.token
        idp = pconf.idp

    # If a domain ID is specified, but not an API key, load the profile with that domain ID
    elif domain_id and not (api_key or provider):
        pconf = auth_conf.get_profile(domain_id=domain_id)
        if pconf is None:
            raise errors.SessionLoadError(
                f"could not find profile with domain ID {domain_id} in profile config"
            )
        name = pconf.name
        api_key = pconf.api_key
        from_conf = True
        token = pconf.token
        idp = pconf.idp

    # If no display name or domain ID were specified, load the active profile from the auth config
    # We deliberately aren't confirming the API key is unset here, due in part to the issue where the
    # Session sets the env var
    elif not domain_id:
        pconf = auth_conf.get_profile()
        if pconf is None:
            raise errors.SessionLoadError("no active profile found")
        name = pconf.name
        domain_id = pconf.domain_id
        api_key = pconf.api_key
        from_conf = True
        token = pconf.token
        idp = pconf.idp

    # If we get to this point without a domain ID and API key or token, we somehow failed to load the domain
    if not domain_id:
        raise errors.SessionLoadError("failed to load domain - no domain ID")
    if not (api_key or token):
        raise errors.SessionLoadError("failed to load domain - no API key or oauth token found")

    # Try to initialize the Session before potentially adding to the config file - if initializing
    # the Session produces an erroneous result, we don't want to add it to the config
    if api_key:
        authn = ApiKeyAuthentication(
            domain_id=domain_id,
            api_key=api_key,
            enable_retries=enable_retries,
        )
    elif token:
        authn = OAuthDomainAuthentication(
            domain_id=domain_id,
            oauth_authentication=GoogleOAuthAuthentication(token, enable_retries=enable_retries),
            identity_provider_name=idp,
        )
    sess = Session(authn)

    # If the flag is set to add to the auth config, and the profile didn't already come from the
    # auth config, then write it to the config, marking as active if that flag is also set
    if (add_to_config or make_active) and not from_conf:
        auth_conf.add_profile(
            domain_id=domain_id,
            api_key=api_key,
            name=name,
            mark_active=make_active,
            write_to_file=True,
            idp=idp,
            token=token,
        )

    # Finally, return the session
    return sess


@dataclass
class EncapsulateResponse:
    """
    EncapsulateResponse contains metadata from encapsulating data, including
    the capsule ID or IDs, and the raw bytes if the capsule was not exported.
    """

    capsule_ids: List[str]
    raw: Optional[bytes]
    load_capsule_func: Optional[
        Callable[[Optional[str], Optional[Union[bytes, "EncapsulateResponse"]], str], Optional[Capsule]]
    ]

    def load(self, read_context: str) -> Optional[Capsule]:
        """
        Load the response into a capsule. Note that this shortcut requires that
        the raw data be returned from the encapsulation.

        :param read_context: The name of the role policy to use for reading data
        :return: The loaded capsule, if the raw data was present on the response.
        """
        return self.load_capsule_func(None, self, read_context)

    def save(self, filename: str):
        """
        Save the capsule to a file
        """
        with open(filename, "wb") as f:
            f.write(self.raw)


class Session(
    CapabilityMixin,
    CapsuleMixin,
    DomainMixin,
    EncryptionMixin,
    FactMixin,
    GeneralMixin,
    IdentityProviderMixin,
    PolicyRuleMixin,
    ReadContextMixin,
    WriteContextMixin,
    VerificationMixin,
    RootEncryptionKeyMixin,
    StarredDomainMixin,
    DataPolicyMixin,
):
    """
    The Session establishes auth and the domain you are working with, providing
    both a standard instantiation or a context manager in which a Capsule and
    its underlying data can be interacted with.
    """

    def __init__(self, authn: Authentication):
        authz = TokenAuthorization(authn)
        self.authz = authz
        self._act_for_domain = None

        super().__init__(authz=self.authz)

    @property
    def domain_id(self):
        """
        Return the current domain ID
        """
        return (
            self._act_for_domain
            if self._act_for_domain is not None
            else self.authz.auth_client.get_domain_id()
        )

    @property
    def api_key(self):
        """
        Return the API key in use by this session
        """
        if not isinstance(self.authz.auth_client, ApiKeyAuthentication):
            raise ValueError("API key is not available for this session")
        return self.authz.auth_client._api_key

    @property
    def session(self):
        return self.authz.get_session()

    @property
    def _email(self) -> Optional[str]:
        """
        Get the email associated with the auth client.
        """
        return self.authz.auth_client.get_email()

    def config(self):
        """
        Returns the configuration of this Session
        """
        return {
            "domain_id": self.domain_id,
            "api_key": self.api_key,
        }

    @classmethod
    def from_api_key(
        cls,
        domain_id: str,
        api_key: str,
        admin_email: Optional[str] = None,
        enable_retries: bool = True,
    ) -> "Session":
        """
        Create a new session with the provided domain ID and API key.

        :param domain_id: The domain ID
        :param api_key: The API key for the domain
        :param admin_email: The admin email for the domain
        :param enable_retries: If True, retry gateway, DNS, and general connection errors
        :return: A Session holding the domain_id and api_key
        """
        authn = ApiKeyAuthentication(
            domain_id, api_key, admin_email=admin_email, enable_retries=enable_retries
        )
        return cls(authn)

    @classmethod
    def from_google_oauth(
        cls,
        domain: str = None,
        identity_provider_name: Optional[str] = None,
        reset_credentials: bool = False,
        token: str = None,
        enable_retries: bool = True,
    ) -> "Session":
        """
        Create a new session authenticated with a Google OAuth token.
        If a domain is provided, the session will be authenticated with that domain and identity provider (default: google).
        If a token is provided, the session will be authenticated with that token. The token refresh is not handled by the session in that case.
        Upstream services should handle the token refresh.

        :param domain: Optional domain ID to authenticate with
        :param identity_provider_name: Optional identity provider name to authenticate with
        :param reset_credentials: If True, any stored oauth credentials will be reset
        :param token: An optional static OAuth token
        :param enable_retries: If True, retry gateway, DNS, and general connection errors
        :return: A Session authenticated with a Google OAuth token
        """
        if token:
            authn = StaticOAuthAuthentication(token, enable_retries=enable_retries)
        else:
            authn = GoogleOAuthAuthentication(
                reset_credentials=reset_credentials, enable_retries=enable_retries
            )
        if domain:
            authn = OAuthDomainAuthentication(
                domain,
                identity_provider_name=identity_provider_name,
                oauth_authentication=authn,
            )
        return cls(authn)

    def new_domain(
        self, admin_email: str, reauthenticate: bool = False, display_name: str = None
    ) -> Dict[str, Any]:
        """
        Create a new domain with the provided email as the admin contact. A
        verification email will be sent to that email. Verification must be completed
        before the Antimatter API can be interacted with.

        :param admin_email: The email address of the domain administrator
        :param reauthenticate: If True, the current session will be reauthenticated with the new domain
        :param display_name: The display name for the new domain
        :return: The domain metadata
        """
        dm = openapi_client.GeneralApi(self.authz.get_client()).domain_add_new(
            openapi_client.NewDomain(admin_email=admin_email, displayName=display_name)
        )
        if self.authz.auth_client.get_token_scope() == "google_oauth_token":
            self.add_starred_domain(dm.id)

        if reauthenticate:
            if isinstance(self.authz.auth_client, (ApiKeyAuthentication, Unauthenticated)):
                self.authz = TokenAuthorization(
                    ApiKeyAuthentication(
                        dm.id,
                        dm.api_key,
                        admin_email=admin_email,
                        enable_retries=self.authz.auth_client.has_client_retry_policy(),
                    )
                )
            elif isinstance(self.authz.auth_client, (GoogleOAuthAuthentication, StaticOAuthAuthentication)):
                self.authz = TokenAuthorization(
                    OAuthDomainAuthentication(dm.id, oauth_authentication=self.authz.auth_client)
                )

        return dm.model_dump()

    def with_domain(self, domain_id: str = None, nickname: str = None, alias: str = None) -> None:
        """
        Use a child domain for the current session.
        Uses the parent's authz to authenticate and authorize all requests.
        Obtains the child domain either by domain ID or nickname or alias.

        :param domain_id: The domain ID of the child domain
        :param nickname: The nickname of the child domain
        :param alias: The alias of the child domain
        """
        if not domain_id and not nickname and not alias:
            raise ValueError("specify a 'domain_id' or 'nickname' when using a child domain")

        if domain_id == "" or domain_id is None:
            domain_id = self.get_peer(nickname=nickname, alias=alias)
            if not domain_id:
                raise ValueError(f"child domain with nickname '{nickname}' or alias '{alias}' not found")
        self._act_for_domain = domain_id
        self.authz.get_session().with_domain(domain_id, nickname, alias)

    def load_capsule(
        self,
        path: Optional[str] = None,
        data: Optional[Union[bytes, EncapsulateResponse]] = None,
        read_context: str = None,
        read_params: Dict[str, str] = {},
    ) -> Optional[Capsule]:
        """
        load_capsule creates a capsule, extracting data from an Antimatter
        Capsule binary blob, either provided in raw bytes or as a string path
        to a local or remote file.

        If the `as_datatype` parameter is supplied and the data is a binary blob
        Antimatter Capsule, the data will be extracted in that format. If the
        data is data for saving to an Antimatter Capsule, `as_datatype` will
        specify the default format for the data when loaded from the blob.

        :param path: The location of the Capsule as a local or remote path.
        :param data: The data to load into an Antimatter Capsule.
        :param read_context: The name of the role policy to use for reading data
        """
        if not read_context:
            raise ValueError("specify a 'read_context' when loading a capsule")

        if not path and not data:
            raise ValueError("specify a 'path' or the raw 'data' when loading a capsule")

        if data and isinstance(data, EncapsulateResponse):
            data = data.raw

        try:
            capsule_session = self.authz.get_session().open_capsule(read_context, read_params, path, data)
            cap = CapsuleBindings(capsule_session)
            capsule = Capsule(capsule_binding=cap)
            return capsule
        except Exception as e:
            raise errors.CapsuleLoadError(e)

    def encapsulate(
        self,
        data: Any = None,
        write_context: str = None,
        span_tags: List[SpanTag] = None,
        column_tags: List[ColumnTag] = None,
        row_tags: List[RowTag] = None,
        as_datatype: Union[Datatype, str] = Datatype.Unknown,
        skip_classify_on_column_names: List[str] = None,
        path: Optional[str] = None,
        subdomains_from: Optional[str] = None,
        create_subdomains: Optional[bool] = False,
        data_file_path: Optional[str] = None,
        data_file_hint: Optional[str] = None,
        **kwargs,
    ) -> EncapsulateResponse:
        """
        Saves the provided Capsule's data, or the provided data using the provided
        write context. If 'as_datatype' is provided, the default datatype for the
        raw data will use the specified type.

        One of 'data' or 'path' must be provided.

        :param data: Raw data in a Capsule-supported format
        :param write_context: The name of the role policy to use for writing data
        :param span_tags: The span tags to manually apply to the data
        :param column_tags: Tags to apply to entire columns by name
        :param row_tags: Tags to apply to entire row by idx
        :param as_datatype: The datatype to override the provided data with when the capsule is read
        :param skip_classify_on_column_names: List of columns to skip classifying
        :param path: If provided, the local or remote path to save the capsule to
        :param subdomains_from: column in the raw data that represents the subdomain
        :param create_subdomains: allow missing subdomains to be created
        :param data_file_path: Optional path to a file containing data to be read. If provided, data from
                this file will be used instead of the 'data' parameter.
        :param data_file_hint: Optional hint indicating the format of the data in the file specified by
                'data_file_hint'. Supported formats include 'json', 'csv', 'txt', 'parquet'.
                If not specified, data will be read as plain text.
        :return: The response containing capsule metadata and the raw blob of the
                capsule if no path was provided.
        """
        if data is None and path is None:
            raise ValueError("specify one of 'data' or 'path' when creating a capsule")

        as_datatype = Datatype(as_datatype)
        if column_tags is None:
            column_tags = []
        if span_tags is None:
            span_tags = []
        if skip_classify_on_column_names is None:
            skip_classify_on_column_names = []

        if not write_context:
            raise ValueError("specify a 'write_context' when creating a capsule")

        if data_file_path:
            if not data_file_hint:
                data_file_hint = infer_filetype(data_file_path)
                if not data_file_hint:
                    raise TypeError("unable to infer data file type, provide 'data_file_hint' argument")
            data = extract_from_file(data_file_path, data_file_hint)

        dt = infer_datatype(data)
        if dt is Datatype.Unknown:
            if as_datatype is Datatype.Unknown:
                raise TypeError("unable to infer type of data, provide 'as_datatype' argument")
            dt = as_datatype

        h = handlers.factory(dt)
        col_names, raw, extra = h.to_generic(data)
        extra = extra_for_session(dt, {**extra, **kwargs})
        jextra = json.dumps(extra)

        # if a cell path is not specified, assume it means the first cell
        for idx, st in enumerate(span_tags):
            if not st.cell_path:
                span_tags[idx].cell_path = f"{col_names[0]}[0]"

        try:
            raw, capsule_ids = self.authz.get_session().encapsulate(
                *Preparer.prepare(
                    col_names, column_tags, row_tags, skip_classify_on_column_names, raw, span_tags, extra
                ),
                write_context,
                [],
                jextra,
                path,
                subdomains_from,
                create_subdomains,
            )
        except Exception as e:
            raise errors.CapsuleSaveError(e)

        if raw is not None:
            raw = bytes(raw)
        return EncapsulateResponse(capsule_ids=capsule_ids, raw=raw, load_capsule_func=self.load_capsule)

    def classify_and_redact(
        self,
        data: Any = None,
        path: Optional[str] = None,
        write_context: str = None,
        span_tags: List[SpanTag] = None,
        column_tags: List[ColumnTag] = None,
        as_datatype: Union[Datatype, str] = Datatype.Unknown,
        skip_classify_on_column_names: List[str] = None,
        read_context: str = None,
        read_parameters: Optional[Dict[str, str]] = {},
        **kwargs,
    ) -> Optional[Capsule]:
        """
        Classifies and redacts the given data or data at a specified path using the
        provided write and read contexts.

        One of 'data' or 'path' must be provided.

        :param data: Raw data to classify and redact
        :param path: Path to the file containing the data
        :param write_context: The write context in which the data is being redacted
        :param span_tags: List of tags for specific data spans
        :param column_tags: Tags for specific columns by name
        :param as_datatype: The expected data type, if known
        :param skip_classify_on_column_names: List of columns to skip classification on
        :param read_context: Read context to use for processing data for read ops
        :param read_parameters: Additional parameters for the read operation
        :return: A Capsule object containing possibly redacted data, or None if an error occurs
        :raises ValueError: If both 'data' and 'path' are missing, or if 'write_context' or 'read_context' is not provided
        :raises TypeError: If the data type cannot be inferred and no 'as_datatype' is specified
        :raises CapsuleLoadError: If classification or redaction fails due to missing or incorrect contexts
        """
        if data is None and path is None:
            raise ValueError("specify one of 'data' or 'path' when classifying and redacting data")

        if write_context is None:
            raise ValueError("specify a 'write_context' when classifying and redacting data")

        if read_context is None:
            raise ValueError("specify a 'read_context_name' when classifying and redacting data")

        as_datatype = Datatype(as_datatype)
        if column_tags is None:
            column_tags = []
        if span_tags is None:
            span_tags = []
        if skip_classify_on_column_names is None:
            skip_classify_on_column_names = []

        dt = infer_datatype(data)
        if dt is Datatype.Unknown:
            if as_datatype is Datatype.Unknown:
                raise TypeError("unable to infer type of data, provide 'as_datatype' argument")
            dt = as_datatype

        h = handlers.factory(dt)
        col_names, raw, extra = h.to_generic(data)

        # if a cell path is not specified, assume it means the first cell
        for idx, st in enumerate(span_tags):
            if not st.cell_path:
                span_tags[idx].cell_path = f"{col_names[0]}[0]"

        try:
            capsule_session = self.authz.get_session().classify_and_redact(
                *Preparer.prepare(
                    col_names, column_tags, [], skip_classify_on_column_names, raw, span_tags, extra
                ),
                [],
                write_context,
                read_context,
                read_parameters,
            )
            cap = CapsuleBindings(capsule_session)
            capsule = Capsule(capsule_binding=cap)
            return capsule
        except Exception as e:
            str_e = str(e).lower()
            if (
                "write_context" in str_e
                or "writecontext" in str_e
                or "failed to create capsule" in str_e
                or "failed to create capsule" in str_e
            ):
                raise errors.CapsuleLoadError(
                    f"failed to classify and redact data: check that write context {write_context} exists for domain : {e}",
                ) from None

            if "read_context" in str_e or "readcontext" in str_e:
                raise errors.CapsuleLoadError(
                    f"failed to classify and redact data: check that read context {read_context} exists for domain",
                ) from None
            raise errors.CapsuleLoadError("classifying and redacting data") from e

    def with_new_peer_domain(
        self,
        import_alias_for_child: str,
        display_name_for_child: str,
        nicknames: Optional[List[str]] = None,
        import_alias_for_parent: Optional[str] = None,
        display_name_for_parent: Optional[str] = None,
        link_all: bool = True,
        link_identity_providers: bool = None,
        link_facts: bool = None,
        link_read_contexts: bool = None,
        link_write_contexts: bool = None,
        link_capabilities: bool = None,
        link_domain_policy: bool = None,
        link_capsule_access_log: bool = None,
        link_control_log: bool = None,
        link_capsule_manifest: bool = None,
    ) -> "Session":
        """
        Creates a new peer domain, returning the authenticated session for that
        new domain.

        :param import_alias_for_child: The import alias for the child domain
        :param display_name_for_child: The display name for the child domain
        :param nicknames: The nicknames for the child domain
        :param import_alias_for_parent: The import alias for the parent domain
        :param display_name_for_parent: The display name for the parent domain
        :param link_all: Link all available resources
        :param link_identity_providers: Link identity providers
        :param link_facts: Link facts
        :param link_read_contexts: Link read contexts
        :param link_write_contexts: Link write contexts
        :param link_capabilities: Link capabilities
        :param link_domain_policy: Link domain policy
        :param link_capsule_access_log: Link capsule access log
        :param link_control_log: Link control log
        :param link_capsule_manifest: Link capsule manifest
        :return: The authenticated session for the new domain
        """
        dm = self.new_peer_domain(
            import_alias_for_child=import_alias_for_child,
            display_name_for_child=display_name_for_child,
            nicknames=nicknames,
            import_alias_for_parent=import_alias_for_parent,
            display_name_for_parent=display_name_for_parent,
            link_all=link_all,
            link_identity_providers=link_identity_providers,
            link_facts=link_facts,
            link_read_contexts=link_read_contexts,
            link_write_contexts=link_write_contexts,
            link_capabilities=link_capabilities,
            link_domain_policy=link_domain_policy,
            link_capsule_access_log=link_capsule_access_log,
            link_control_log=link_control_log,
            link_capsule_manifest=link_capsule_manifest,
        )
        return Session.from_api_key(
            dm.id, dm.api_key, enable_retries=self.authz.auth_client.has_client_retry_policy()
        )

    def get_admin_url(
        self,
        company_name: str,
        peer_domain_id: Optional[str] = None,
        nickname: Optional[str] = None,
        alias: Optional[str] = None,
        token_lifetime: Optional[int] = None,
    ) -> Optional[str]:
        """
        Generate the admin URL for the domain. By default, this is the domain
        for this session. If one of the peer_domain_id, nickname, or alias are
        provided, the admin URL will be generated for the subdomain that
        matches.

        :param company_name: The name of the company to display
        :param peer_domain_id: The domain ID of the peer
        :param nickname: The nickname for the peer domain
        :param alias: One of the aliases of the peer domain
        :param token_lifetime: How long the token should last for, in seconds
        :return: The admin URL
        """
        if not peer_domain_id and (nickname or alias):
            peer_domain_id = self.get_peer(nickname=nickname, alias=alias)

        # Re-authenticate prior to generating a token so that we get one with the
        # full correct lifetime.
        self.authz.auth_client.authenticate(token_lifetime=token_lifetime)

        api_client = self.authz.get_client()
        auth_api = openapi_client.AuthenticationApi(api_client=api_client)

        _id = self.domain_id
        tkn = api_client.configuration.access_token
        if peer_domain_id:
            _id = peer_domain_id
            tkn = auth_api.domain_authenticate(
                domain_id=peer_domain_id,
                domain_authenticate=openapi_client.DomainAuthenticate(token=tkn),
                token_exchange=True,
            ).token

        url = urlparse(api_client.configuration.host)
        url = f"{url.scheme}://{url.netloc}".replace("api", "app").replace("8080", "3000")
        company_name = quote_plus(company_name)
        tkn = quote_plus(tkn)
        return f"{url}/settings/{_id}/byok?vendor={company_name}&token={tkn}"
