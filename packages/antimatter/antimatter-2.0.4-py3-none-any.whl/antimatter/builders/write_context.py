from typing import Union

import antimatter_api as openapi_client
from antimatter.constants import Hook, WriteContextHookMode


class WriteContextBuilder:
    """
    Builder class for creating WriteContext objects.
    """

    def __init__(self) -> None:
        """
        Initialize a new instance of WriteContextBuilder.
        """
        self.write_context = openapi_client.AddWriteContext(
            summary="",
            description="",
            config=openapi_client.WriteContextConfigInfo(
                requiredHooks=[],
                keyReuseTTL=0,
            ),
        )

    def set_summary(self, summary: str) -> "WriteContextBuilder":
        """
        Set the summary of the WriteContext.

        :param summary: The summary to set.
        :return: The WriteContextBuilder instance.
        """
        self.write_context.summary = summary
        return self

    def set_description(self, description: str) -> "WriteContextBuilder":
        """
        Set the description of the WriteContext.

        :param description: The description to set.
        :return: The WriteContextBuilder instance.
        """
        self.write_context.description = description
        return self

    def add_hook(
        self,
        name: Union[Hook, str],
        constraint: str = ">1.0.0",
        mode: Union[WriteContextHookMode, str] = WriteContextHookMode.Sync,
    ) -> "WriteContextBuilder":
        """
        Add a hook to the WriteContext.

        :param name: The name of the hook.
        :param constraint: The constraint of the hook.
        :param mode: The mode of the hook.
        :return: The WriteContextBuilder instance.
        """
        self.write_context.config.required_hooks.append(
            openapi_client.WriteContextConfigInfoRequiredHooksInner(
                hook=name,
                constraint=constraint,
                mode=WriteContextHookMode(mode).value,
            )
        )
        return self

    def set_key_reuse_ttl(self, seconds: int) -> "WriteContextBuilder":
        """
        Set the recommended key reuse TTL, which instructs the client
        to reuse encryption keys (and associated capsule IDs) for up
        to this duration in seconds.

        :param seconds: The TTL in seconds to set.
        :return: The WriteContextBuilder instance.
        """
        self.write_context.config.key_reuse_ttl = seconds
        return self

    def build(self) -> openapi_client.AddWriteContext:
        """
        Build the WriteContext.

        :return: The built WriteContext.
        """
        return self.write_context


class WriteContextConfigurationBuilder:
    """
    Builder class for creating WriteContextConfigInfo objects.
    """

    def __init__(self) -> None:
        """
        Initialize a new instance of WriteContextConfigurationBuilder.
        """
        self._write_context_config = openapi_client.WriteContextConfigInfo(requiredHooks=[], keyReuseTTL=0)

    def add_hook(
        self,
        name: Union[Hook, str],
        constraint: str = ">1.0.0",
        mode: Union[WriteContextHookMode, str] = WriteContextHookMode.Sync,
    ) -> "WriteContextConfigurationBuilder":
        """
        Add a hook to the WriteContextConfigurationBuilder.

        :param name: The name of the hook.
        :param constraint: The constraint of the hook.
        :param mode: The mode of the hook.
        :return: The WriteContextConfigurationBuilder instance.
        """
        self._write_context_config.required_hooks.append(
            openapi_client.WriteContextConfigInfoRequiredHooksInner(
                hook=name,
                constraint=constraint,
                mode=WriteContextHookMode(mode).value,
            )
        )
        return self

    def set_key_reuse_ttl(self, seconds: int) -> "WriteContextConfigurationBuilder":
        """
        Set the recommended key reuse TTL, which instructs the client
        to reuse encryption keys (and associated capsule IDs) for up
        to this duration in seconds.

        :param seconds: The TTL in seconds to set.
        :return: The WriteContextConfigurationBuilder instance.
        """
        self._write_context_config.key_reuse_ttl = seconds
        return self

    def build(self) -> openapi_client.WriteContextConfigInfo:
        """
        Build the WriteContextConfigInfo.

        :return: The built WriteContextConfigInfo.
        """
        return self._write_context_config
