# https://francetravail.io/data/api/rome?tabgroup-api=documentation&doc-section=api-doc-section-caracteristiques
import logging

from requests import exceptions

from ...base import Api as BaseApi
from ...cache import session

logger = logging.getLogger("poleemploi_io_api.rome.v4")


class ApiMetier(BaseApi):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # params
        self.url = self._verify_param(
            "url",
            "https://api.francetravail.io/partenaire/rome-metiers/v1/metiers",
            **kwargs,
        )

    def scope(self) -> str:
        return "api_rome-metiersv1 nomenclatureRome"

    def _api_error(self, err, **kwargs):
        logger.error(err)
        logger.error(kwargs)
        return None

    def _get(self, url: str, kwargs: dict):
        # headers
        headers = kwargs.pop("headers", {})
        headers = self.get_auth_header(headers)

        # params
        params = [(k, kwargs[k]) for k in kwargs.keys()]

        kwargs = {
            "url": url,
            "params": params,
            "headers": headers,
            "timeout": self.timeout,
        }
        try:
            r = session.get(**kwargs)
        except exceptions.Timeout as e:
            return self._api_error(e, **kwargs)
        except exceptions.TooManyRedirects as e:
            return self._api_error(e, **kwargs)
        except exceptions.RequestException as e:
            return self._api_error(e, **kwargs)

        return r

    def theme(self, **kwargs):
        """Call to endpoint : [https://api.francetravail.io/partenaire/rome-metiers/v1/metiers/theme](https://api.francetravail.io/partenaire/rome-metiers/v1/metiers/theme)
        Rules:
            If `code` in kwargs then the call will be made to `theme/code`

            Else the endpoint will be `theme/`

        Returns:
            response (requests.Response):
        """
        url = self.url + "/theme"

        code: str = kwargs.pop("code", None)
        if code:
            url += f"/{code.upper()}"

        return self._get(url, kwargs)

    def metier(self, **kwargs):
        """Call to endpoint : [https://api.francetravail.io/partenaire/rome-metiers/v1/metiers/metier](https://api.francetravail.io/partenaire/rome-metiers/v1/metiers/metier)
        Rules:
            If `code` in kwargs then the call will be made to `metier/code`

            Else the endpoint will be `metier/`

        Returns:
            response (requests.Response):
        """
        url = self.url + "/metier"
        code: str = kwargs.pop("code", None)
        if code:
            url += f"/{code.upper()}"
        return self._get(url, kwargs)

    def granddomain(self, **kwargs):
        """Call to endpoint : [https://api.francetravail.io/partenaire/rome-metiers/v1/metiers/grand-domaine](https://api.francetravail.io/partenaire/rome-metiers/v1/metiers/grand-domaine)
        Rules:
            If `code` in kwargs then the call will be made to `grand-domaine/code`

            Else the endpoint will be `grand-domaine/`

        Returns:
            response (requests.Response):
        """
        url = self.url + "/grand-domaine"
        code: str = kwargs.pop("code", None)
        if code:
            url += f"/{code.upper()}"
        return self._get(url, kwargs)

    def domaineprofessionnel(self, **kwargs):
        """Call to endpoint : [https://api.francetravail.io/partenaire/rome-metiers/v1/metiers/domaine-professionnel](https://api.francetravail.io/partenaire/rome-metiers/v1/metiers/domaine-professionnel)
        Rules:
            If `code` in kwargs then the call will be made to `domaine-professionnel/code`

            Else the endpoint will be `domaine-professionnel/`

        Returns:
            response (requests.Response):
        """
        url = self.url + "/domaine-professionnel"
        code: str = kwargs.pop("code", None)
        if code:
            url += f"/{code.upper()}"
        return self._get(url, kwargs)

    def appellation(self, **kwargs):
        """Call to endpoint : [https://api.francetravail.io/partenaire/rome-metiers/v1/metiers/appellation](https://api.francetravail.io/partenaire/rome-metiers/v1/metiers/appellation)
        Rules:
            If `code` in kwargs then the call will be made to `appellation/code`

            If `q` in kwargs then the call will be made to `appellation/requete`

            Otherwise the endpoint will be `appellation/`

        Returns:
            response (requests.Response):
        """
        url = self.url + "/appellation"
        code: int = kwargs.pop("code", None)
        query = kwargs.get("q")
        if code:
            url += f"/{code}"
        elif query:
            url += "/requete"

        return self._get(url, kwargs)
