from bs4 import BeautifulSoup

from models import (
    AccountLoginFormData,
    ConnectAuthorizeFormData,
    SignInOidcFormData,
)

__all__ = (
    'parse_sign_in_oidc_form_data',
    'parse_connect_authorize_form_data',
    'parse_account_login_form_data',
)


def parse_sign_in_oidc_form_data(
        sign_in_oidc_form_html: str,
) -> SignInOidcFormData:
    soup = BeautifulSoup(sign_in_oidc_form_html, 'lxml')

    code = soup.find(attrs={'name': 'code'}).get('value')
    scope = soup.find(attrs={'name': 'scope'}).get('value')
    state = soup.find(attrs={'name': 'state'}).get('value')
    session_state = soup.find(attrs={'name': 'session_state'}).get('value')

    return SignInOidcFormData(
        code=code,
        scope=scope,
        state=state,
        session_state=session_state,
    )


def parse_account_login_form_data(
        account_login_form_html: str,
        username: str,
        password: str,
        country_code: str,
) -> AccountLoginFormData:
    soup = BeautifulSoup(account_login_form_html, 'lxml')

    return_url = soup.find(attrs={'name': 'returnUrl'}).get('value')
    request_verification_token = (
        soup.find(attrs={'name': '__RequestVerificationToken'}).get('value')
    )

    return AccountLoginFormData(
        return_url=return_url,
        username=username,
        password=password,
        tenant_name='dodopizza',
        country_code=country_code,
        auth_method='local',
        remember_login=True,
        request_verification_token=request_verification_token,
    )


def parse_connect_authorize_form_data(
        connect_authorize_form_html: str,
) -> ConnectAuthorizeFormData:
    soup = BeautifulSoup(connect_authorize_form_html, 'lxml')

    client_id = soup.find(attrs={'name': 'client_id'}).get('value')
    redirect_uri = soup.find(attrs={'name': 'redirect_uri'}).get('value')
    response_type = soup.find(attrs={'name': 'response_type'}).get('value')
    scope = soup.find(attrs={'name': 'scope'}).get('value')
    code_challenge = soup.find(attrs={'name': 'code_challenge'}).get('value')
    code_challenge_method = (
        soup.find(attrs={'name': 'code_challenge_method'}).get('value')
    )
    response_mode = soup.find(attrs={'name': 'response_mode'}).get('value')
    nonce = soup.find(attrs={'name': 'nonce'}).get('value')
    state = soup.find(attrs={'name': 'state'}).get('value')

    return ConnectAuthorizeFormData(
        client_id=client_id,
        redirect_uri=redirect_uri,
        response_type=response_type,
        scope=scope,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
        response_mode=response_mode,
        nonce=nonce,
        state=state,
    )
