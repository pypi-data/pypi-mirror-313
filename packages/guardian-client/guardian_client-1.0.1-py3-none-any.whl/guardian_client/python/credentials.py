import os
from datetime import datetime, timedelta, timezone

import jwt

import requests
import logging
import random
from urllib.parse import urlparse

from typing import Optional

logger = logging.getLogger(__name__)


class GuardianClientInvalidConfigException(Exception):
    """
    Raised when required environment variables for the client are missing.
    """


class InvalidAuthTokenException(Exception):
    """
    Raised when we fail to obtain an access token from the auth provider
    """


class GuardianClientCredentialContext:
    GUARDIAN_SCANNER_CLIENT_ID = "GUARDIAN_SCANNER_CLIENT_ID"
    GUARDIAN_SCANNER_CLIENT_SECRET = "GUARDIAN_SCANNER_CLIENT_SECRET"

    def __init__(self, guardian_endpoint: str) -> None:
        # Guardian endpoint is suffixed with /guardian, but we want just the hostname
        self.guardian_endpoint = guardian_endpoint
        base_url_parts = urlparse(self.guardian_endpoint)
        self._token_endpoint = f"{base_url_parts.scheme}://{base_url_parts.netloc}/auth/v1/client_auth/token"

        # authentication credentials
        self._client_id = os.getenv(self.GUARDIAN_SCANNER_CLIENT_ID)
        self._client_secret = os.getenv(self.GUARDIAN_SCANNER_CLIENT_SECRET)
        for val, name in [
            (self._client_id, self.GUARDIAN_SCANNER_CLIENT_ID),
            (self._client_secret, self.GUARDIAN_SCANNER_CLIENT_SECRET),
        ]:
            if not val:
                logger.error(f"Failed to read {name} from the environment")
                raise GuardianClientInvalidConfigException(
                    f"Failed to read {name} from the environment"
                )

        self._access_token = None
        logger.info(f"New guardian-client credential context initializaed")

    @property
    def access_token(self) -> str:
        if not self._access_token or self._is_credential_expired():
            # request for a fresh token and return when done.
            logger.info(
                f"Existing access token is {'not present' if not self._access_token else 'expired'}; fetching a new token from token endpoint"
            )
            self._access_token = self._load_access_token()

        return self._access_token

    def _load_access_token(self) -> str:
        # SDK is authenticated using the Client Credential flow
        access_token = self._request_access_token(
            token_url=str(self._token_endpoint),
            client_id=str(self._client_id),
            client_secret=str(self._client_secret),
        )

        if access_token is None:
            logger.critical(
                f"""
                Failed to obtain an access token. Check the logs for more information. 
                Make sure env variables are properly set.
                """
            )
            raise InvalidAuthTokenException("Failed to obtain an access token")

        logger.debug("Obtained a valid access token from auth provider")

        return access_token

    def _is_credential_expired(self) -> bool:
        if not self._access_token:
            raise InvalidAuthTokenException("Access token is not valid")

        token_exp = self._get_token_expiration_timestamp(self._access_token)

        expiration_datetime = datetime.fromtimestamp(token_exp, tz=timezone.utc)

        # Add a random jitter to space out the token refreshes
        jitter = random.randint(10, 30)
        return datetime.now(timezone.utc) > expiration_datetime - timedelta(
            seconds=jitter
        )

    def _get_token_expiration_timestamp(self, token: str) -> str:
        try:
            decoded_token = jwt.decode(token, options={"verify_signature": False})

            return decoded_token.get("exp")
        except jwt.DecodeError as e:
            logger.critical("Failed to decode JWT access token", exc_info=e)
            raise InvalidAuthTokenException("Access token is not valid")

    def _request_access_token(
        self,
        token_url: str,
        client_id: str,
        client_secret: str,
    ) -> Optional[str]:
        """
        Retrieves a JWT access token using client credentials flow.

        Arguments:
            token_url: The URL of the /token endpoint on the API we're calling
            client_id: The client ID
            client_secret: The client secret
        """
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
        }

        response = requests.post(
            token_url,
            json=payload,
            timeout=2,
        )

        access_token = response.json().get("access_token")
        if access_token and type(access_token) is str:
            return access_token
        else:
            raise InvalidAuthTokenException(
                "Access token requests failed; check if client credentials are correct"
            )
