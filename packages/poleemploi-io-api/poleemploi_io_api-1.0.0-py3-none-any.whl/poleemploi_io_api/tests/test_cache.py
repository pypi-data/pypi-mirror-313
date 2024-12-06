import os
import time
from unittest import TestCase

import requests

from .. import RomeV4
from ..cache import session

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

WAIT_TIME = 0.2


class TestRegion(TestCase):
    def setUp(self) -> None:
        self.api = RomeV4(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        return super().setUp()

    def domaineprofessionnel(self) -> requests.Response:

        if not os.environ.get("REQUEST_CACHE"):
            # deactivate test if locally defined sqlite or

            r = self.api.domaineprofessionnel()
            assert not r.from_cache

        else:
            r = self.api.domaineprofessionnel()
            assert not r.from_cache
            assert r.status_code == 200

            time.sleep(WAIT_TIME)
            r = self.api.domaineprofessionnel()
            assert r.from_cache
            assert r.status_code == 200

    def test_cache(self) -> None:

        self.api.domaineprofessionnel()

        # Get some debugging info about the cache
        print(session.cache)
        print("Cached URLS:")
        print("\n".join(session.cache.urls()))

        assert len(session.cache.urls()) > 0

    def test_retry_after(self) -> None:
        s = time.time()
        try:
            r = session.get("https://httpbin.org/status/502", timeout=180)
            print(r.status_code)
        except Exception as e:
            print(e)
        e = time.time()

        assert (e - s) > 12
