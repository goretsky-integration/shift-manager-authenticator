from contextlib import contextmanager

import httpx

from models import AuthHttpClient, ShiftManagerHttpClient

__all__ = (
    'closing_shift_manager_http_client',
    'closing_auth_http_client',
)


@contextmanager
def closing_auth_http_client() -> AuthHttpClient:
    with httpx.Client(
            headers={'User-Agent': 'dodoextbot'},
            base_url='https://auth.dodois.io',
    ) as http_client:
        yield AuthHttpClient(http_client)


@contextmanager
def closing_shift_manager_http_client(
        country_code: str,
) -> ShiftManagerHttpClient:
    url = f'https://shiftmanager.dodopizza.{country_code}'
    with httpx.Client(
            headers={'User-Agent': 'dodoextbot'},
            base_url=url,
    ) as http_client:
        yield ShiftManagerHttpClient(http_client)
