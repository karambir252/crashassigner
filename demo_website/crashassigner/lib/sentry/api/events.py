from typing import List
from .client import SentryClient
from ..models.event import SentryEvent


class SentryEventsApi:
    def __init__(self, client: SentryClient):
        self.client = client

    def get_latest_event(self, issue_id) -> SentryEvent:
        api_point = 'issues/{}/events/latest/'.format(
            issue_id
        )
        event_data = self.client.get(api_point)
        return SentryEvent(event_data)
