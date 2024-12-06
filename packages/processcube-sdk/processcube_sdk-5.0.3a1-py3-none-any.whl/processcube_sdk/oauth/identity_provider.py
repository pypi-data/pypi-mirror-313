import logging
import os
import sys

from oauth2_client.credentials_manager import CredentialManager, ServiceInformation
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, after_log
from requests import exceptions

logger = logging.getLogger('processcube.oauth')

MAX_GET_OAUTH_ACCESS_TOKEN_RETRIES = os.environ.get(
    'MAX_GET_OAUTH_ACCESS_TOKEN_RETRIES', 10)


def exit_after_retries(retry_state):
    logger.error(
        f'Failed all {retry_state.attempt_number} retries. Now exitin.')
    sys.exit(1)


class IdentityProvider:

    def __init__(self, authority_url: str, client_name: str, client_secret: str, client_scopes: str):
        self._authority_url = authority_url
        self._client_name = client_name
        self._client_secret = client_secret
        self._client_scopes = client_scopes

        self._access_token_caller = self._prepare_get_access_token_caller()
        logger.debug(f"Prepare identity provider with (authority_url={authority_url}, client_name={client_name}, client_secret=***, client_scopes={client_scopes}).")

    def __call__(self):

        return self._access_token_caller()

    def _prepare_get_access_token_caller(self):

        @retry(
            stop=stop_after_attempt(MAX_GET_OAUTH_ACCESS_TOKEN_RETRIES),
            wait=wait_exponential(multiplier=1, min=2, max=30),
            retry=retry_if_exception_type(exceptions.ConnectionError),
            after=after_log(logger, logging.ERROR),
            retry_error_callback=exit_after_retries,
        )
        def get_access_token(authority_url, client_name, client_secret, client_scopes):
            logger.debug(f"Get access token from ProcessCube (authority_url={authority_url}, client_name={client_name}, client_secret=***, client_scopes={client_scopes}).")

            client_scopes = client_scopes.split(' ')

            service_information = ServiceInformation(f'{authority_url}/auth',
                                                     f'{authority_url}/token',
                                                     client_name,
                                                     client_secret,
                                                     client_scopes)
            manager = CredentialManager(service_information)

            manager.init_with_client_credentials()

            return {'token': manager._access_token}

        return lambda: get_access_token(self._authority_url, self._client_name, self._client_secret, self._client_scopes)
