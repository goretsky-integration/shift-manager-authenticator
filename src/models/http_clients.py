from typing import NewType

import httpx

__all__ = (
    'AuthHttpClient',
    'ShiftManagerHttpClient',
    'AuthCredentialsStorageApiConnectionHttpClient',
)

AuthHttpClient = NewType('AuthHttpClient', httpx.Client)
ShiftManagerHttpClient = NewType('ShiftManagerHttpClient', httpx.Client)
AuthCredentialsStorageApiConnectionHttpClient = (
    NewType('AuthCredentialsStorageApiConnectionHttpClient', httpx.Client)
)
