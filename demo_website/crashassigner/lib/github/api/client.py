import json
from graphqlclient import GraphQLClient


class GithubClient:
    def __init__(self, api_token):
        self.api_token = api_token
        self.client = GraphQLClient('https://api.github.com/graphql')
        self.client.inject_token('bearer ' + api_token)

    def get(self, query):
        result = self.client.execute(query)
        data = json.loads(result)
        return data
