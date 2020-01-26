from .client import GithubClient
from .files import GithubFilesAPI
from .blames import GithubBlamesAPI


class GithubAPI:
    def __init__(self, api_token):
        self.client = GithubClient(api_token)
        self.files = GithubFilesAPI(self.client)
        self.blames = GithubBlamesAPI(self.client)
