from typing import Union

import antimatter_api as openapi_client
from antimatter.constants import Hook


class ReadContextBuilder:
    """
    A builder class for constructing a ReadContext object.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the ReadContextBuilder class.
        """
        self.read_context = openapi_client.AddReadContext(
            summary="",
            description="",
            readParameters=[],
            requiredHooks=[],
            keyCacheTTL=0,
            disableReadLogging=False,
        )

    def set_summary(self, summary: str) -> "ReadContextBuilder":
        """
        Sets the summary of the ReadContext.

        :param summary: The summary to set.
        :return: The instance of the builder.
        """
        self.read_context.summary = summary
        return self

    def set_description(self, description: str) -> "ReadContextBuilder":
        """
        Sets the description of the ReadContext.

        :param description: The description to set.
        :return: The instance of the builder.
        """
        self.read_context.description = description
        return self

    def add_required_hook(
        self, name: Union[Hook, str], constraint: str = ">1.0.0", write_context: str = None
    ) -> "ReadContextBuilder":
        """
        Adds a required hook to the ReadContext.

        :param name: The name of the hook.
        :param constraint: The constraint of the hook.
        :param write_context: The write context for the hook

        :return: The instance of the builder.
        """
        self.read_context.required_hooks.append(
            openapi_client.ReadContextRequiredHook(
                hook=name,
                constraint=constraint,
                write_context=write_context,
            )
        )
        return self

    def add_read_parameter(self, key: str, required: bool, description: str) -> "ReadContextBuilder":
        """
        Adds a read parameter to the ReadContext.

        :param key: The key of the parameter.
        :param required: Whether the parameter is required.
        :param description: The description of the parameter.

        :return: The instance of the builder.
        """
        self.read_context.read_parameters.append(
            openapi_client.ReadContextParameter(
                key=key,
                required=required,
                description=description,
            )
        )
        return self

    def set_key_cache_ttl(self, ttl: int) -> "ReadContextBuilder":
        """
        Sets the recommended TTL for client-side CapsuleOpenResponses
        associated with this ReadContext.

        :param ttl: The TTL to set.
        :return: The instance of the builder.
        """
        self.read_context.key_cache_ttl = ttl
        return self

    def set_disable_read_logging(self) -> "ReadContextBuilder":
        """
        Instructs the client that read logging associated with this
        ReadContext can be skipped, which speeds up access to capsules.

        :return: This instance of the builder.
        """
        self.read_context.disable_read_logging = True
        return self

    def build(self) -> openapi_client.AddReadContext:
        """
        Builds the ReadContext and returns it.

        :return: The built ReadContext.
        """
        return self.read_context
