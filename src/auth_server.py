from models import AuthCredentialsStorageApiConnectionHttpClient

__all__ = ('AuthCredentialsStorageApiConnection',)


class AuthCredentialsStorageApiConnection:

    def __init__(
            self,
            http_client: AuthCredentialsStorageApiConnectionHttpClient,
    ):
        self.__http_client = http_client

    def save_cookies(self, account_name: str, cookies: dict[str, str]) -> bool:
        url = '/auth/cookies/'
        request_data = {'account_name': account_name, 'cookies': cookies}
        response = self.__http_client.patch(url, json=request_data)
        return response.is_success
