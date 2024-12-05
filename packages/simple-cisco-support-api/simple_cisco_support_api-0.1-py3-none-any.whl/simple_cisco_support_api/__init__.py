from .rest_client.api import API
from .rest_client.resource import Resource
from .rest_client.request import make_request
from .rest_client.models import Request
from types import MethodType

import logging
from pprint import pformat
import urllib.parse


class CiscoTokenAPIResource(Resource):
    pass


class CiscoSupportAPI(Resource):
    pass


class CiscoSupportAPIClient(object):
    def __init__(self, url="https://apix.cisco.com/", **kwargs):
        self._log = logging.getLogger()
        self._base_url = url
        self._grant_type = kwargs.get("grant_type", "client_credentials")
        self._login_url = kwargs.get(
            "login_url", "https://id.cisco.com/oauth2/default/v1/"
        )
        self.tokenapi = API(
            api_root_url=self._login_url,  # base api url
            params={},  # default params
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },  # default headers
            timeout=10,  # default timeout in seconds
            append_slash=False,  # append slash to final url
            json_encode_body=False,  # encode body as json
            ssl_verify=kwargs.get("ssl_verify", True),
            resource_class=CiscoTokenAPIResource,
            log_curl_commands=kwargs.get("log_curl_commands", False),
        )
        self.api = API(
            api_root_url=url,  # base api url
            params={},  # default params
            headers={},  # default headers
            timeout=10,  # default timeout in seconds
            append_slash=False,  # append slash to final url
            json_encode_body=True,  # encode body as json
            ssl_verify=kwargs.get("ssl_verify", True),
            resource_class=CiscoSupportAPI,
            log_curl_commands=kwargs.get("log_curl_commands", False),
        )

    def __str__(self):
        return pformat(self.api.get_resource_list())

    def login(self, client_id=None, client_secret=None):
        if client_id:
            self._client_id = client_id
        if client_secret:
            self._client_secret = client_secret

        auth_data = self.tokenapi.token.create(
            body=urllib.parse.urlencode(
                {
                    "grant_type": self._grant_type,
                    "client_id": client_id,
                    "client_secret": client_secret,
                }
            ),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token = auth_data.get("access_token")
        self.api.headers["Authorization"] = f"Bearer {token}"
        return True
