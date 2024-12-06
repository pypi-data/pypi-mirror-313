import os
from unittest import TestCase

from .. import BaseApi

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
TOKEN_URL = os.environ.get("TOKEN_URL", "https://entreprise.francetravail.fr")


class MyApi(BaseApi):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # you must define the scope function to be able to set the scopes excpected for your api
    def scope(self) -> str:
        return "api_romev1 nomenclatureRome"


class TestBaseApi(TestCase):
    def setUp(self) -> None:
        self.api = MyApi(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_url=TOKEN_URL
        )
        self.api._get_access_token()
        return super().setUp()

    def test_access_token(self) -> None:
        self.assertTrue(self.api._access_token is not None)

    def test_auth_header_empty(self) -> None:
        header = self.api.get_auth_header()
        self.assertTrue(header is not None)

    def test_auth_header_non_empty(self) -> None:
        # headers must not be affected
        header = self.api.get_auth_header({"foo": "bar"})
        self.assertTrue("foo" in header)
        self.assertTrue("Authorization" in header)


class TestBaseNoParamApi(TestCase):

    def test_token_url(self) -> None:
        api = MyApi(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token_url=None)
        self.assertTrue(api._token_url is not None)
