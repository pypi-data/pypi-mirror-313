import os
from copy import deepcopy
from os.path import expanduser, isfile
from pathlib import Path
from typing import Any, Dict, List, Optional
from pathlib import Path

import safer
import yaml

from antimatter.auth.config.global_identity import GlobalIdentity
from antimatter.auth.config.tokens import OidcTokenFactory, OidcToken
from antimatter.auth.config.profiles import Profile

SUPPORTED_SCHEMA_VERSIONS = ["v1"]
SUPPORTED_TOKEN_TYPES = ["google"]
_SCHEMA_KEY = "schema"
_PROFILES_KEY = "profiles"
_ACTIVE_PROFILE_KEY = "active_profile"
_GLOBAL_IDENT_KEY = "global_identities"
_ACTIVE_GLOBAL_IDENT_KEY = "active_global_identity"
_DEFAULT_CONFIG_PATH = os.path.join(Path.home(), ".antimatter", "config")


class AuthConfig:
    """
    The AuthConfig is responsible for interacting with the config file and locally
    storing profile and identity information.
    """

    schema: str
    profiles: List[Profile]
    active_profile: Optional[str]
    global_identities: List[GlobalIdentity]
    active_global_identity: Optional[str]
    _path: str

    def __init__(self):
        """
        Initialize an AuthConfig with default empty values.
        """
        self.schema = SUPPORTED_SCHEMA_VERSIONS[-1]
        self.profiles = []
        self.active_profile = None
        self.global_identities = []
        self.active_global_identity = None

    @staticmethod
    def from_dict(conf_dict: Optional[Dict[str, Any]]) -> "AuthConfig":
        """
        Load an AuthConfig from a json serializable dictionary in the expected config format.

        :param conf_dict: The json serializable dictionary to parse into an AuthConfig
        :return: The parsed AuthConfig
        """
        if conf_dict is None:
            # If no dictionary was provided, use an empty one to parse a config with default empty values
            conf_dict = {}

        # Parse the schema version, using the latest version if none found in the config
        schema_version = conf_dict.get(_SCHEMA_KEY, SUPPORTED_SCHEMA_VERSIONS[-1])
        if schema_version is None:
            raise ValueError(
                f"auth config '{_SCHEMA_KEY}' version not specified; must be one of {SUPPORTED_SCHEMA_VERSIONS}"
            )
        if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
            raise ValueError(
                f"auth config 'schema' version not supported: {conf_dict.get(_SCHEMA_KEY)}. "
                f"Must be in {SUPPORTED_SCHEMA_VERSIONS}"
            )

        conf = AuthConfig()
        conf.schema = schema_version
        conf.profiles = [Profile.from_dict(prof) for prof in conf_dict.get(_PROFILES_KEY, [])]
        conf.active_profile = conf_dict.get(_ACTIVE_PROFILE_KEY, None)
        conf.global_identities = [
            GlobalIdentity.from_dict(glob_id) for glob_id in conf_dict.get(_GLOBAL_IDENT_KEY, [])
        ]
        conf.active_global_identity = conf_dict.get(_ACTIVE_GLOBAL_IDENT_KEY, None)
        conf.add_observers()
        return conf

    def add_observers(self):
        for profile in self.profiles:
            if profile.token is not None:
                profile.token.add_observer(self.to_file)
        for global_identity in self.global_identities:
            global_identity.token.add_observer(self.to_file)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert an AuthConfig into a dictionary.

        :return: The dictionary containing AuthConfig values
        """
        _dict = {
            _SCHEMA_KEY: self.schema,
            _PROFILES_KEY: [],
            _ACTIVE_PROFILE_KEY: None,
            _GLOBAL_IDENT_KEY: [],
            _ACTIVE_GLOBAL_IDENT_KEY: None,
        }

        if self.profiles:
            _dict[_PROFILES_KEY] = [prof.to_dict() for prof in self.profiles]
        if self.active_profile:
            _dict[_ACTIVE_PROFILE_KEY] = self.active_profile
        if self.global_identities:
            _dict[_GLOBAL_IDENT_KEY] = [global_ident.to_dict() for global_ident in self.global_identities]
        if self.active_global_identity:
            _dict[_ACTIVE_GLOBAL_IDENT_KEY] = self.active_global_identity
        return _dict

    @staticmethod
    def from_file(path: str = None) -> "AuthConfig":
        """
        Load an AuthConfig from a config file.

        :param path: Override path to the config file. If not provided, default path will be used
        :return: The parsed AuthConfig
        """
        if not path:
            path = _DEFAULT_CONFIG_PATH
        # Ensure we expand any path containing the '~' home directory directive
        path = expanduser(path)

        parsed = None
        if isfile(path):
            with open(path, "r") as f:
                parsed = yaml.safe_load(f)
        conf = AuthConfig.from_dict(parsed)
        conf._path = path  # Save the path for writing to file
        return conf

    def to_file(self, path: str = None) -> None:
        """
        Save the values in the AuthConfig into the config file. Note that this
        will create the file and parent directories if it does not exist, and
        will overwrite the file if it does exist.

        :param path: Override path to the config file. If not provided, default path will be used
        """
        if not path:
            path = self._path
        # Ensure we expand any path containing the '~' home directory directive
        path = expanduser(path)

        # Create the file and any parent directories if they don't exist. We
        # use fname.parent to make the directory as the default filename of
        # 'config' will result in a directory being created
        fname = Path(path)
        fname.parent.mkdir(parents=True, exist_ok=True)
        fname.touch(exist_ok=True)

        serialized = self.to_dict()
        with safer.open(path, "w", temp_file=True) as f:
            yaml.safe_dump(serialized, f)

    def add_profile(
        self,
        domain_id: str,
        api_key: str = None,
        name: Optional[str] = None,
        default_read_context: Optional[str] = None,
        default_write_context: Optional[str] = None,
        mark_active: bool = False,
        write_to_file: bool = False,
        path: Optional[str] = None,
        token: Optional[OidcToken] = None,
        idp: Optional[str] = None,
    ) -> None:
        """
        Add a profile to the AuthConfig with the provided domain ID and API key. If
        no display name is provided, the domain ID will be used. If write_to_file is
        set to True, the updated AuthConfig will be written to the file it was loaded
        from, or the override path.

        :param domain_id: The domain ID for the profile
        :param api_key: The API key for the profile
        :param name: The display name for the profile
        :param default_read_context: The default read context
        :param default_write_context: The default write context
        :param mark_active: If True, mark this profile as active
        :param write_to_file: If True, overwrite the config file with the updated contents of the AuthConfig
        :param path: Override path to the config file
        :param token: The OIDC token for the profile (mutually exclusive with API key)
        :param idp: The identity provider for the OIDC token
        """
        if name is None:
            name = domain_id

        # Short circuit exit if a profile already exists by this name
        if self.get_profile(name=name):
            return

        prof = Profile(
            name=name,
            domain_id=domain_id,
            api_key=api_key,
            default_read_context=default_read_context,
            default_write_context=default_write_context,
            token=token,
            idp=idp,
        )
        self.profiles.append(prof)
        if mark_active:
            self.active_profile = name
        if write_to_file:
            self.to_file(path=path)

    def update_profile(
        self,
        name: str,
        domain_id: str,
        api_key: Optional[str] = None,
        token: Optional[OidcToken] = None,
        idp: Optional[str] = None,
        default_read_context: Optional[str] = None,
        default_write_context: Optional[str] = None,
        write_to_file: bool = False,
        path: Optional[str] = None,
    ):
        """
        Update a profile with the provided domain ID and API key. If write_to_file is
        set to True, the updated AuthConfig will be written to the file it was loaded
        from, or the override path.

        :param name: The display name of the profile to update
        :param domain_id: The domain ID for the profile
        :param api_key: The API key for the profile
        :param token: The token for the profile
        :param idp: The identity provider for the OIDC token
        :param default_read_context: The default read context
        :param default_write_context: The default write context
        :param write_to_file: If True, overwrite the config file with the updated contents of the AuthConfig
        :param path: Override path to the config file
        """
        prof = self.get_profile(name=name)
        if prof is None:
            raise ValueError(f"No profile found with name '{name}'")

        prof.domain_id = domain_id
        prof.api_key = api_key
        prof.idp = idp
        prof.token = token
        prof.default_read_context = default_read_context
        prof.default_write_context = default_write_context
        if write_to_file:
            self.to_file(path=path)

    def add_global_identity(
        self,
        token_type: str,
        name: str,
        mark_active: bool = False,
        write_to_file: bool = False,
        path: Optional[str] = None,
        **kwargs,
    ) -> None:
        """
        Add a global identity to the AuthConfig with the provided token type, name,
        and kwargs for initializing the global identity token. If write_to_file is
        set to True, the updated AuthConfig will be written to the file it was loaded
        from, or the override path.

        :param token_type: The token type for the global identity
        :param name: The display name for the global identity
        :param mark_active: If True, mark this global identity as active
        :param write_to_file: If True, overwrite the config file with the updated contents of the AuthConfig
        :param path: Override path to the config file
        :param kwargs: The kwargs with which to initialize the global identity token
        """
        token = OidcTokenFactory.from_cli_type(token_type)
        global_ident = GlobalIdentity(name=name, token=token(**kwargs))
        self.global_identities.append(global_ident)
        if mark_active:
            self.active_global_identity = name
        if write_to_file:
            self.to_file(path=path)

    def update_global_identity(
        self,
        name: str,
        token_type: str,
        write_to_file: bool = False,
        path: Optional[str] = None,
        **kwargs,
    ) -> None:
        """
        Update a global identity with the provided token type and kwargs. If write_to_file
        is set to True, the updated AuthConfig will be written to the file it was loaded
        from, or the override path.

        :param name: The display name of the global identity to update
        :param token_type: The token type for the global identity
        :param write_to_file: If True, overwrite the config file with the updated contents of the AuthConfig
        :param path: Override path to the config file
        :param kwargs: The kwargs with which to initialize the global identity token
        """
        global_ident = self.get_global_identity(name)
        if global_ident is None:
            raise ValueError(f"No global identity found with name '{name}'")

        token = OidcTokenFactory.from_cli_type(token_type)
        global_ident.token = token(**kwargs)
        if write_to_file:
            self.to_file(path=path)

    def get_profile(self, name: Optional[str] = None, domain_id: Optional[str] = None) -> Optional[Profile]:
        """
        Get the profile using either the name or domain_id. Name has higher
        precedence if both are provided. If neither are provided, the active
        profile will be used.

        :param name: The display name of the profile to find
        :param domain_id: The domain ID of the profile to find
        :return: The found profile, or None if not found
        """
        if name is None and domain_id is None:
            name = self.active_profile

        if name is not None:
            for profile in self.profiles:
                if profile.name == name:
                    return deepcopy(profile)

        if domain_id is not None:
            for profile in self.profiles:
                if profile.domain_id == domain_id:
                    return deepcopy(profile)

        return None

    def mark_profile_active(
        self,
        name: Optional[str] = None,
        domain_id: Optional[str] = None,
        write_to_file: bool = False,
        path: Optional[str] = None,
    ) -> None:
        """
        Mark the profile with the given name or domain_id as active. If domain_id
        is provided, it must be present in the known profiles in order to fetch
        the name.

        :param name: The display name of the profile to mark as active
        :param domain_id: The domain ID of the profile to mark as active
        :param write_to_file: If True, overwrite the config file with the updated contents of the AuthConfig
        :param path: Override path to the config file
        """
        if name is None and domain_id is None:
            raise ValueError("one of 'name' or 'domain_id' must be provided")

        if name is None:
            for profile in self.profiles:
                if profile.domain_id == domain_id:
                    name = profile.name
                    break
            else:
                raise ValueError(f"domain_id '{domain_id}' could not be matched to known name")

        self.active_profile = name
        if write_to_file:
            self.to_file(path=path)

    def get_global_identity(
        self,
        name: Optional[str] = None,
    ) -> Optional[GlobalIdentity]:
        """
        Get the global identity with the given name.

        :param name: The name of the global identity to find
        :return: The found global identity, or None if not found
        """
        if name is None:
            name = self.active_global_identity

        if name is not None:
            for ident in self.global_identities:
                if ident.name == name:
                    return deepcopy(ident)

        return None

    def mark_global_identity_active(
        self,
        name: str,
        write_to_file: bool = False,
        path: Optional[str] = None,
    ) -> None:
        """
        Mark the global identity with the given name as active.

        :param name: The name of the global identity to mark as active
        :param write_to_file: If True, overwrite the config file with the updated contents of the AuthConfig
        :param path: Override path to the config file
        """
        self.active_global_identity = name
        if write_to_file:
            self.to_file(path=path)
