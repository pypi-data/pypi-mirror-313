import requests

from .schemas import Token


class Api:

    def _verify_param(self, value, default_value=None, **kwargs):

        if kwargs.get(value):
            data = kwargs.get(value)
        elif default_value:
            data = default_value
        else:
            raise ValueError(f"No {value} provided")

        return data

    def __init__(self, **kwargs):
        # params

        self._token_url = self._verify_param(
            "token_url", "https://entreprise.francetravail.fr", **kwargs
        )

        self._client_secret = self._verify_param("client_secret", **kwargs)

        self._client_id = self._verify_param("client_id", **kwargs)

        self._access_token = None

        self.timeout = int(
            self._verify_param(
                "timeout",
                30,
                **kwargs,
            )
        )

    def scope(self) -> str:
        """This method enables you to define the scope for your api.

        Raises:
            NotImplementedError: You must define this function to define the scope of the token
        """
        raise NotImplementedError(
            "You must define this function to define the scope of the token"
        )

    def _get_access_token(self):
        """This method sets the access token to be used on your api.

        Raises:
            ValueError: If poleemploi.io raises a status_code different from 200
        """
        scope = self.scope()

        params = {
            "grant_type": "client_credentials",
            "scope": scope,
        }
        data = {"client_secret": self._client_secret, "client_id": self._client_id}

        r = requests.post(
            self._token_url + "/connexion/oauth2/access_token?realm=%2Fpartenaire",
            params=params,
            data=data,
            timeout=self.timeout,
        )

        if r.status_code != 200:
            raise ValueError(
                f"Could not read token from api. status_code={r.status_code} response={r.content}"
            )

        self._access_token = Token(**r.json())

    def get_auth_header(self, header=None):
        """If an access token was found, this method returns the provided header
        with the Authorization added.

        Args:
            header (dict, optional): this is the header you want to use for your api call.
        """
        if not self._access_token:
            self._get_access_token()

        if not header:
            header = {}

        header["Authorization"] = (
            f"{self._access_token.token_type} {self._access_token.access_token}"
        )

        return header
