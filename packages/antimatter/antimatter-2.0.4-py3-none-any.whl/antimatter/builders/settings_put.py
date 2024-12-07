from dataclasses import dataclass
from enum import Enum
from typing import Union, List

import antimatter_api as openapi_client


@dataclass
class SettingsPutBuilder:
    """
    A builder class for constructing a Settings object.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the ReadContextBuilder class.
        """
        self.settings = openapi_client.NewDomainSettings(
            active_admin_contacts=None,
            pending_admin_contacts=None,
            default_display_name=None,
            default_token_lifetime=None,
            maximum_token_lifetime=None,
        )

    def set_default_display_name(self, name: str) -> "SettingsPutBuilder":
        """
        Sets the active_admin_contacts of the domain settings.

        :param name: The new default display name
        :return: The instance of the builder.
        """
        self.settings.default_display_name = name
        return self

    def set_default_token_lifetime(self, lifetime: int) -> "SettingsPutBuilder":
        """
        Sets the set_default_token_lifetime of the domain settings.

        :param lifetime: The new default token lifetime
        :return: The instance of the builder.
        """
        self.settings.default_token_lifetime = lifetime
        return self

    def set_maximum_token_lifetime(self, lifetime: int) -> "SettingsPutBuilder":
        """
        Sets the maximum_token_lifetime of the domain settings.

        :param lifetime: The new maximin token lifetime
        :return: The instance of the builder.
        """
        self.settings.maximum_token_lifetime = lifetime
        return self

    def set_active_admin_contacts(self, contacts: List[str]) -> "SettingsPutBuilder":
        """
        Sets the set_active_admin_contacts of the domain settings.
        Note: this list cannot contain any new contacts and should only be
        used to remove current active admin contacts. To add new active
        admin contacts, fist add the contacts to the pending contacts list
        using `set_pending_admin_contacts`. Once updated, a verification
        request will then be sent to the contact, and once verified,
        the contact will be converted into an active admin contact.

        :param contacts: The new list of active admin contacts
        :return: The instance of the builder.
        """
        self.settings.active_admin_contacts = contacts
        return self

    def set_pending_admin_contacts(self, contacts: List[str]) -> "SettingsPutBuilder":
        """
        Sets the pending_admin_contacts of the domain settings.

        :param contacts: The new list of pending admin contacts
        :return: The instance of the builder.
        """
        self.settings.pending_admin_contacts = contacts
        return self

    def build(self) -> openapi_client.NewDomainSettings:
        """
        Builds the NewDomainSettings and returns it.

        :return: The built NewDomainSettings.
        """
        return self.settings
