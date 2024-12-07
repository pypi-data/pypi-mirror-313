from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, Iterator, List, Optional, Union

import antimatter_api as openapi_client
from dateutil.relativedelta import relativedelta

from antimatter import CapsuleTag, ColumnTag, SpanTag, location
from antimatter.builders.settings_put import SettingsPutBuilder
from antimatter.session_mixins.serializers.identity_details import serialize_identity_provider_info_dict

from antimatter.session_mixins.base import BaseMixin
from antimatter.tags.tag import get_tag_name
from antimatter.utils.time import get_time_range


class GeneralMixin(BaseMixin):
    """
    Session mixin defining CRUD functionality for other general functionality.
    """

    _page_res_size: int = 100

    def get_private_info(self) -> openapi_client.DomainPrivateInfo:
        """
        Returns a Domain's summary information.

        :return: The private summary info for a domain
        """
        return openapi_client.DomainPrivateInfo.from_json(self.authz.get_session().get_private_info())

    def get_public_info(self) -> openapi_client.DomainPublicInfo:
        """
        Returns a Domain's summary information. This endpoint does not require
        authorization

        :return: The public summary info for a domain
        """
        return openapi_client.DomainPublicInfo.from_json(self.authz.get_session().get_public_info())

    def get_settings(self) -> openapi_client.DomainSettings:
        """
        Return the domain settings.
        """
        return openapi_client.DomainSettings.from_json(self.authz.get_session().get_settings())

    def put_settings(self, settings: SettingsPutBuilder) -> openapi_client.DomainSettings:
        """
        Updates the domain settings with the provided settings.

        :param settings: The domain settings to be updated.
        :return: The domain settings after applying the proposed updates
        """
        return openapi_client.DomainSettings.from_json(
            self.authz.get_session().put_settings(settings.build().to_json())
        )

    def get_status(self) -> openapi_client.DomainStatus:
        """
        Return the domain status, which contains important notifications for
        administrators of the domain.
        """
        return openapi_client.DomainStatus.from_json(self.authz.get_session().get_status())

    def list_hooks(self) -> List[openapi_client.DomainHooksListHooksInner]:
        """
        Return a list of available hooks in this domain. A hook is a data processor,
        like a PII classifier
        """
        return openapi_client.DomainHooksList.from_json(self.authz.get_session().list_hooks()).hooks

    def list_resources(self) -> List[openapi_client.DomainResourceSummarySchemaInner]:
        """
        Return a list of resource strings that can be used in policy rules, and
        the set of permissions that you can assign to them.
        """
        return openapi_client.DomainResourceSummary.from_json(
            self.authz.get_session().list_resources()
        ).var_schema

    def query_access_log(
        self,
        start_date: Optional[Union[datetime, str]] = None,
        end_date: Optional[Union[datetime, str]] = None,
        duration: Optional[Union[timedelta, relativedelta, str]] = None,
        session: Optional[str] = None,
        location: Optional[str] = None,
        location_prefixed: Optional[bool] = None,
        operation_type: Optional[str] = None,
        allowed_tag: Optional[Union[str, CapsuleTag, ColumnTag, SpanTag]] = None,
        redacted_or_tokenized_tag: Optional[Union[str, CapsuleTag, ColumnTag, SpanTag]] = None,
        capsule_id: Optional[str] = None,
    ) -> Iterator[openapi_client.AccessLogEntry]:
        """
        Query the data access log for this domain. This contains all operations
        interacting with capsules within this domain. An iterator is returned
        over the results in reverse chronological order.

        :param start_date: The earlier date of the date range. As results are returned in reverse
                    chronological order, this date corresponds with the end of the result set.
                    This should be a timezone-aware datetime, or else will be treated as the
                    system timezone
        :param end_date: The later date of the date range. As results are returned in reverse
                    chronological order, this date corresponds with the beginning of the result
                    set. If not specified, defaults to the current time.
                    This should be a timezone-aware datetime, or else will be treated as the
                    system timezone
        :param duration: The query time range duration. This can be a timedelta or a string such
                    as '2h'. When using duration, by default the query time range ends 'now',
                    unless one of start_date or end_date is specified. If both start_date and end_date
                    are specified, duration is ignored. If using a string value, valid time units are
                    "ns", "us" (or "µs"), "ms", "s", "m", "h", "d", "mo", "y". These can be grouped
                    together, such as 1h5m30s
        :param session: The session you would like to filter on. This will return results for only
                    the provided session. If not specified, this field is ignored
        :param location: The location you would like to filter on. This is a matched filter and will
                    return results starting with the provided string. If not specified, this
                    field is ignored
        :param location_prefixed: A boolean indicator to indicate that the location you provided is a prefix
                    or not. If this is set to true, then the filter provided in location is
                    treated as a prefix. If not specified, this is treated as false
        :param operation_type: The operation you would like to filter on. This will filter on the provided
                    operation type and return all results using the provided operation type. If
                    not specified, this field is ignored
        :param allowed_tag: The allow tag key you would like to filter on. This accepts tag key only
                    and will return all allowed tag results matching the provided tag key. If
                    not specified, this field is ignored
        :param redacted_or_tokenized_tag: The redacted or tokenized tag key you would like to filter on. This accepts
                    a tag key only and will return all redacted and tokenized tag key results
                    matching the provided tag key. If not specified, this field is ignored
        :param capsule_id: The ID for a specific capsule. Use this to limit results to a single capsule
        :return: An iterator over the access logs matching the filters
        """
        pagination = None
        has_more = True
        start_date, end_date = get_time_range(start_date=start_date, end_date=end_date, duration=duration)
        allowed_tag = get_tag_name(allowed_tag)
        redacted_or_tokenized_tag = get_tag_name(redacted_or_tokenized_tag)

        start_date = (
            start_date.strftime("%Y-%m-%dT%H:%M:%SZ") if isinstance(start_date, datetime) else start_date
        )
        end_date = end_date.strftime("%Y-%m-%dT%H:%M:%SZ") if isinstance(end_date, datetime) else end_date

        while has_more:
            kwargs = {
                "start_date": start_date,
                "end_date": end_date,
                "num_results": self._page_res_size,
                "start_from_id": pagination,
                "session": session,
                "location": location,
                "location_prefixed": location_prefixed,
                "operation_type": operation_type,
                "allowed_tag": allowed_tag,
                "redacted_or_tokenized_tag": redacted_or_tokenized_tag,
            }
            if capsule_id is None:
                res = openapi_client.CapsulesApi(self.authz.get_client()).domain_query_access_log(
                    domain_id=self.domain_id, **kwargs
                )
            else:
                res = openapi_client.AccessLogResults.from_json(
                    self.authz.get_session().query_access_logs(**kwargs)
                )
            has_more = res.has_more
            for log in res.results:
                pagination = log.id
                yield log

    def query_control_log(
        self,
        start_date: Optional[Union[datetime, str]] = None,
        end_date: Optional[Union[datetime, str]] = None,
        duration: Optional[Union[timedelta, relativedelta, str]] = None,
        session: Optional[str] = None,
        url: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Iterator[openapi_client.DomainControlLogEntry]:
        """
        Query the domain control-plane audit log. An iterator is returned over the
        results in reverse chronological order.

        :param start_date: The earlier date of the date range. As results are returned in reverse
                    chronological order, this date corresponds with the end of the result set.
                    This should be a timezone-aware datetime, or else will be treated as the
                    system timezone
        :param end_date: The later date of the date range. As results are returned in reverse
                    chronological order, this date corresponds with the beginning of the
                    result set. If not specified, defaults to the current time.
                    This should be a timezone-aware datetime, or else will be treated as the
                    system timezone
        :param duration: The query time range duration. This can be a timedelta or a string such
                    as '2h'. When using duration, by default the query time range ends 'now',
                    unless one of start_date or end_date is specified. If both start_date and end_date
                    are specified, duration is ignored. If using a string value, valid time units are
                    "ns", "us" (or "µs"), "ms", "s", "m", "h", "d", "mo", "y". These can be grouped
                    together, such as 1h5m30s
        :param session: The session you would like to filter on. This will return results for only
                    the provided session. If not specified, this field is ignored
        :param url: The URL you would like to filter on. This is a prefix matched filter and
                    will return results starting with the provided string. If not specified,
                    this field is ignored
        :param description: The description you would like to filter on. This is an in matched filter
                    and will return results that  contain the provided string. If not specified,
                    this field is ignored
        :return: An iterator over the control logs matching the filters
        """
        pagination = None
        has_more = True
        start_date, end_date = get_time_range(start_date=start_date, end_date=end_date, duration=duration)

        start_date = (
            start_date.strftime("%Y-%m-%dT%H:%M:%SZ") if isinstance(start_date, datetime) else start_date
        )
        end_date = end_date.strftime("%Y-%m-%dT%H:%M:%SZ") if isinstance(end_date, datetime) else end_date

        while has_more:
            res = openapi_client.DomainControlLogResults.from_json(
                self.authz.get_session().query_control_log(
                    start_date=start_date,
                    end_date=end_date,
                    num_results=self._page_res_size,
                    start_from_id=pagination,
                    session=session,
                    url=url,
                    description=description,
                )
            )
            has_more = res.has_more
            for log in res.results:
                pagination = log.id
                yield log
