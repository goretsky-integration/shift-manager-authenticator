from typing import NewType

import httpx

__all__ = ('AuthHttpClient', 'ShiftManagerHttpClient')

AuthHttpClient = NewType('AuthHttpClient', httpx.Client)
ShiftManagerHttpClient = NewType('ShiftManagerHttpClient', httpx.Client)
