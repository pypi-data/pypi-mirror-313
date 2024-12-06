import requests

from ... import auth


class ApiError(Exception):
    pass


class Client:
    _class_reasoner = None

    def __init__(self, reasoner=None, api_key=None, host=None, api_version=None):
        self._reasoner = reasoner or self._class_reasoner
        if self._reasoner is None:
            raise ValueError("Please provide a reasoner")
        self._api_key = auth.get_api_key(api_key)
        self._host = host or "api.imandra.ai"
        self._api_version = api_version or "v1beta1"
        self._headers = {"Authorization": f"Bearer {self._api_key}"}

    def eval(self, input: str):
        url = (
            f"https://{self._host}/{self._api_version}/reasoners/{self._reasoner}/eval"
        )
        response = requests.post(url, headers=self._headers, json={"input": input})

        if response.status_code != 200:
            raise ApiError(response)

        return response.json()
