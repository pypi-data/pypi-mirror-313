import requests
from requests.auth import HTTPBasicAuth


def default_on_response(response: requests.Response) -> dict:
    """
    :param response:
    :return: the input response
    :raise HTTPError: if status_code is not OK(200)
    """
    if response.status_code != 200:
        response.raise_for_status()
    else:
        return response.json()


class Request:
    def __init__(self, url: str, auth: dict = None, on_response=default_on_response):
        self.url = url
        if auth is not None:
            self.auth = HTTPBasicAuth(auth['username'], auth['password'])
        self.on_response = on_response

    def get(self, params=None, **kwargs) -> dict:
        kwargs.setdefault('auth', getattr(self, 'auth', None))
        response = requests.get(self.url, params, **kwargs)
        return self.on_response(response)

    def post(self, json=None, data=None, **kwargs) -> dict:
        kwargs.setdefault('auth', getattr(self, 'auth', None))
        response = requests.post(self.url, data, json, **kwargs)
        return self.on_response(response)
