from typing import Any, Dict, List
from urllib.parse import urlparse

import antimatter_api as openapi_client
from antimatter import errors

from antimatter.session_mixins.base import BaseMixin


class StarredDomainMixin(BaseMixin):

    def _verify_call(self):
        if self.authz.auth_client.get_token_scope() != "google_oauth_token":
            raise errors.PermissionDenied("use an oauth client to access this functionality")
        return

    def list_starred_domains(self) -> List[str]:
        """
        Returns a list of starred domains for the current user
        """
        self._verify_call()
        return openapi_client.StarredDomainList.from_json(
            self.authz.get_session().list_starred_domains()
        ).domains

    def add_starred_domain(self, domain_id: str) -> None:
        """
        Adds a domain to the starred list for the current user
        """
        self._verify_call()
        self.authz.get_session().add_starred_domain(domain_id)

    def delete_starred_domain(self, domain_id: str) -> None:
        """
        Removes a domain from the starred list for the current user
        """
        self._verify_call()
        self.authz.get_session().delete_starred_domain(domain_id)

    def invite_url(self, domain_id: str) -> str:
        """
        Returns the invite url for the given domain. If you navigate to this URL,
        it will add the domain to your starred domains
        """
        api_client = self.authz.get_client()

        url = urlparse(api_client.configuration.host)
        url = f"{url.scheme}://{url.netloc}".replace("api", "app").replace("8080", "3000")
        return f"{url}/add/{domain_id}"
