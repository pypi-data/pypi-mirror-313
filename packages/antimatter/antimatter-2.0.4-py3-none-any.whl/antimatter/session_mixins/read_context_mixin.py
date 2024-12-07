from typing import Any, Callable, Dict, List

import antimatter_api as openapi_client
from antimatter.builders import ReadContextBuilder

from antimatter.session_mixins.base import BaseMixin


class ReadContextMixin(BaseMixin):
    """
    Session mixin defining CRUD functionality for read contexts.
    """

    def add_read_context(self, name: str, builder: ReadContextBuilder) -> None:
        """
        Upserts a read context for the current domain and auth

        :param name: The name of the read context to add or update
        :param builder: The builder containing read context configuration
        """
        if builder is None:
            raise ValueError("Read context builder is required")
        self.authz.get_session().add_read_context(name, builder.build().to_json())

    def list_read_context(self) -> List[openapi_client.ReadContextShortDetails]:
        """
        Returns a list of read contexts available for the current domain and auth
        """
        return openapi_client.ReadContextList.from_json(
            self.authz.get_session().list_read_context()
        ).read_contexts

    def describe_read_context(self, name: str) -> openapi_client.ReadContextDetails:
        """
        Returns the read context with the given name for the current domain and auth

        :param name: The name of the read context to describe
        :return: The full details of the read context
        """
        return openapi_client.ReadContextDetails.from_json(
            self.authz.get_session().describe_read_context(name)
        )

    def delete_read_context(self, name: str) -> None:
        """
        Delete a read context. All configuration associated with this read
        context will also be deleted. Domain policy rules referencing this read
        context will be left as-is.

        :param name: The name of the read context to delete
        """
        self.authz.get_session().delete_read_context(name)
