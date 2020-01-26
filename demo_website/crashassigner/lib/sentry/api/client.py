import requests


class ApiException(Exception):
    pass


class SentryClient:
    def __init__(self, api_token, server=None):
        if server is None:
            server = 'https://sentry.io'
        self.api_token = api_token
        self.server = server
        self.base_url = '{}/api/0'.format(server)

    def get(self, api_point):
        url = '{}/{}'.format(self.base_url, api_point)
        response = requests.get(
            url,
            headers={
                'Authorization': 'Bearer {}'.format(self.api_token)
            }
        )

        if response.status_code != 200:
            msg = str(response.status_code) + ' : ' + str(response.content)
            raise ApiException(msg)

        return response.json()
