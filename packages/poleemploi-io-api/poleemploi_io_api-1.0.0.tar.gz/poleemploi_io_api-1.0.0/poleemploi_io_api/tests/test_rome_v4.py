import os
import time
from unittest import TestCase

from .. import RomeV4

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
TOKEN_URL = os.environ.get("TOKEN_URL", "https://entreprise.francetravail.fr")
ROMEV4_URL = os.environ.get(
    "ROMEV4_URL", "https://api.francetravail.io/partenaire/rome-metiers/v1/metiers"
)
WAIT_TIME = 1


class TestRomeV4(TestCase):
    def setUp(self) -> None:
        self.api = RomeV4(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            url=ROMEV4_URL,
            token_url=TOKEN_URL,
        )
        self.api._get_access_token()
        return super().setUp()

    def test_scope(self) -> None:
        self.assertTrue(self.api.scope() == "api_rome-metiersv1 nomenclatureRome")

    def test_theme(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.theme()
        self.assertTrue(r.status_code == 200)

        time.sleep(WAIT_TIME)
        r = self.api.theme(code="01")
        self.assertTrue(r.status_code == 200)

    def test_metier(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.metier(**{"code-naf": "10"})
        self.assertTrue(r.status_code == 200)

        time.sleep(WAIT_TIME)
        r = self.api.metier(code="D1102")
        self.assertTrue(r.status_code == 200)

    def test_appellation(self) -> None:
        time.sleep(WAIT_TIME)

        r = self.api.appellation()
        self.assertTrue(r.status_code == 200)

        time.sleep(WAIT_TIME)
        r = self.api.appellation(code=17541)
        self.assertTrue(r.status_code == 200)

    def test_granddomain(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.granddomain()
        self.assertTrue(r.status_code == 200)

    def test_domaineprofessionnel(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.domaineprofessionnel()
        self.assertTrue(r.status_code == 200)
