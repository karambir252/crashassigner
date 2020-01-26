from .client import SentryClient
from .issues import SentryIssuesApi
from .events import SentryEventsApi


class SentryAPI:
    def __init__(self, api_token, server=None):
        self.client = SentryClient(api_token)
        self.issues = SentryIssuesApi(self.client)
        self.events = SentryEventsApi(self.client)
