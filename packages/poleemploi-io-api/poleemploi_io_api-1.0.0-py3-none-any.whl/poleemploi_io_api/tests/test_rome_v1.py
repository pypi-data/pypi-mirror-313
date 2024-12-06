import os
import time
from unittest import TestCase

from .. import RomeV1

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
WAIT_TIME = 1
TOKEN_URL = os.environ.get("TOKEN_URL", "https://entreprise.francetravail.fr")
ROMEV1_URL = os.environ.get(
    "ROMEV1_URL", "https://api.francetravail.io/partenaire/rome/v1/"
)


class TestRomeV1(TestCase):

    def setUp(self) -> None:
        self.api = RomeV1(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            url=ROMEV1_URL,
            token_url=TOKEN_URL,
        )
        self.api._get_access_token()
        return super().setUp()

    def test_scope(self) -> None:
        self.assertTrue(self.api.scope() == "api_romev1 nomenclatureRome")

    def test_appellation(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.appellation(code=11579)
        self.assertTrue(r.status_code == 200)

    def test_appellation_by_codes(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.appellation(codes=[11579])
        self.assertTrue(r.status_code == 200)

    def test_metier(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.metier(q="chocolats", qf="competencesDeBase(libelle)")
        self.assertTrue(r.status_code == 200)

    def test_domaineprofessionnel(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.domaineprofessionnel()
        self.assertTrue(r.status_code == 200)
