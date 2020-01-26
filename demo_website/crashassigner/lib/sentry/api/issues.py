from typing import List
from .client import SentryClient
from ..models.issue import SentryIssue


class SentryIssuesApi:
    def __init__(self, client: SentryClient):
        self.client = client

    def get_list(self, organization, project) -> List[SentryIssue]:
        api_point = 'projects/{}/{}/issues/'.format(
            organization,
            project
        )
        issues_data = self.client.get(api_point)
        return [SentryIssue(d) for d in issues_data]
