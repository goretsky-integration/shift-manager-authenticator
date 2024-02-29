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
    print(sign_in_oidc_form_html)
    soup = BeautifulSoup(sign_in_oidc_form_html, 'lxml')

    code = (soup.find('input', attrs={'name': 'code'}) or {}).get('value')
    scope = (soup.find('input', attrs={'name': 'scope'}) or {}).get('value')
    state = (soup.find('input', attrs={'name': 'state'}) or {}).get('value')
    session_state = (
        (soup.find('input', attrs={'name': 'session_state'}) or {}).get('value')
    )

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

    return_url = (soup.find('input', attrs={'name': 'ReturnUrl'}) or {}).get('value')
    request_verification_token = (
        (soup.find('input', attrs={'name': '__RequestVerificationToken'}) or {})
        .get('value')
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

    client_id = (soup.find(attrs={'name': 'client_id'}) or {}).get('value')
    redirect_uri = (
        (soup.find(attrs={'name': 'redirect_uri'}) or {}).get('value')
    )
    response_type = (
        (soup.find(attrs={'name': 'response_type'}) or {}).get('value')
    )
    scope = (soup.find(attrs={'name': 'scope'}) or {}).get('value')
    code_challenge = (
        (soup.find(attrs={'name': 'code_challenge'}) or {}).get('value')
    )
    code_challenge_method = (
        (soup.find(attrs={'name': 'code_challenge_method'}) or {}).get('value')
    )
    response_mode = (
        (soup.find(attrs={'name': 'response_mode'}) or {}).get('value')
    )
    nonce = (soup.find(attrs={'name': 'nonce'}) or {}).get('value')
    state = (soup.find(attrs={'name': 'state'}) or {}).get('value')

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
