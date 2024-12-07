from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Iterator, List, Optional, Union

import antimatter_api as openapi_client
from dateutil.relativedelta import relativedelta

from antimatter.tags import CapsuleTag
from antimatter.cap_prep.applicator import TAG_SOURCE, TAG_VERSION

from antimatter.session_mixins.base import BaseMixin
from antimatter.utils.time import get_time_range


class CapsuleMixin(BaseMixin):
    """
    Session mixin defining CRUD functionality for capsules and tags.
    """

    _page_res_size: int = 100

    def list_capsules(
        self,
        start_date: Optional[Union[datetime, str]] = None,
        end_date: Optional[Union[datetime, str]] = None,
        duration: Optional[Union[timedelta, relativedelta, str]] = None,
        span_tag: Optional[str] = None,
        sort_on: Optional[str] = None,
        ascending: Optional[bool] = None,
    ) -> Iterator[openapi_client.CapsuleInfo]:
        """
        Returns an iterator over the capsules available for the current domain and auth

        :param start_date:
            The earlier date of the date range. As results are returned in reverse chronological order, this date
            corresponds with the end of the result set. This should be a timezone-aware datetime, or else will be
            treated as the system timezone
        :param end_date:
            The later date of the date range. As results are returned in reverse chronological order, this date
            corresponds with the beginning of the result set. If not specified, defaults to the current time.
            This should be a timezone-aware datetime, or else will be treated as the system timezone
        :param duration: The query time range duration. This can be a timedelta or a string such
            as '2h'. When using duration, by default the query time range ends 'now',
            unless one of start_date or end_date is specified. If both start_date and end_date
            are specified, duration is ignored. If using a string value, valid time units are
            "ns", "us" (or "µs"), "ms", "s", "m", "h", "d", "mo", "y". These can be grouped
            together, such as 1h5m30s.
        :param span_tag:
            The span tag you would like to filter on. This accepts a tag key only and will return all span tag key
            results matching the provided tag key. If not specified, this field is ignored.
        :param sort_on:
            The capsule field you would like to sort on. This accepts the field only and will return results ordered
            on the provided field. If not specified, this field is ignored.
        :param ascending:
            This defines whether a sorted result should be order ascending. This accepts a boolean value and when true
            will work in combination with the sort_on and start_after parameters to return values in ascending order.
            If not specified, this field is ignored and treated as false.
        """
        pagination = None
        start_date, end_date = get_time_range(start_date=start_date, end_date=end_date, duration=duration)

        while True:
            res = openapi_client.CapsuleList.from_json(
                self.authz.get_session().list_capsules(
                    start_date=start_date,
                    end_date=end_date,
                    num_results=self._page_res_size,
                    span_tags=span_tag,
                    sort_on=sort_on,
                    start_after=pagination,
                    ascending=ascending,
                )
            )
            if not res.results:
                break
            for capsule in res.results:
                pagination = capsule.page_key
                yield capsule

    def get_capsule_info(self, capsule_id: str) -> openapi_client.CapsuleInfo:
        """
        Get the summary information about the capsule.

        :param capsule_id: The identifier for the capsule
        :return: The summary information about the capsule
        """
        return openapi_client.CapsuleInfo.from_json(
            self.authz.get_session().get_capsule_info(capsule_id=capsule_id)
        )

    def upsert_capsule_tags(self, capsule_id: str, tags: List[CapsuleTag]) -> None:
        """
        Upsert the capsule-level tags to apply to a capsule.

        :param capsule_id: The capsule to apply tags to
        :param tags: The tags to apply to the capsule
        """
        self.authz.get_session().upsert_capsule_tags(
            capsule_id=capsule_id,
            tags=[
                openapi_client.Tag(
                    name=tag.name,
                    value=tag.tag_value,
                    type=tag.tag_type.name.lower(),
                    hook_version=f"{TAG_VERSION[0]}.{TAG_VERSION[1]}.{TAG_VERSION[2]}",
                    source=TAG_SOURCE,
                ).to_json()
                for tag in tags
            ],
        )

    def delete_capsule_tags(self, capsule_id: str, tag_names: List[str]) -> None:
        """
        Delete capsule-level tags

        :param capsule_id: The capsule to delete tags from
        :param tag_names: The names of the tags to delete
        """
        self.authz.get_session().delete_capsule_tags(
            capsule_id=capsule_id,
            tags=openapi_client.DeleteTags(names=tag_names).to_json(),
        )
