import contextlib

import httpx

from models import (
    AuthCredentialsStorageApiConnectionHttpClient,
    AuthHttpClient,
    ShiftManagerHttpClient,
)

__all__ = (
    'closing_shift_manager_http_client',
    'closing_auth_http_client',
    'closing_auth_credentials_storage_api_connection_http_client',
)


@contextlib.contextmanager
def closing_auth_http_client() -> AuthHttpClient:
    with httpx.Client(
            headers={'User-Agent': 'dodoextbot'},
            base_url='https://auth.dodois.io',
            follow_redirects=True,
    ) as http_client:
        yield AuthHttpClient(http_client)


@contextlib.contextmanager
def closing_shift_manager_http_client(
        country_code: str,
) -> ShiftManagerHttpClient:
    url = f'https://shiftmanager.dodopizza.{country_code}'
    with httpx.Client(
            headers={'User-Agent': 'dodoextbot'},
            base_url=url,
            follow_redirects=True,
    ) as http_client:
        yield ShiftManagerHttpClient(http_client)


@contextlib.contextmanager
def closing_auth_credentials_storage_api_connection_http_client(
        api_base_url: str,
) -> AuthCredentialsStorageApiConnectionHttpClient:
    with httpx.Client(base_url=api_base_url) as http_client:
        yield AuthCredentialsStorageApiConnectionHttpClient(http_client)
