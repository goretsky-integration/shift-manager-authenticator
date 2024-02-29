from uuid import UUID

import httpx
import structlog.stdlib
from structlog.contextvars import bound_contextvars

from config import load_accounts
from connections import DodoConnection
from http_clients import (
    closing_auth_http_client,
    closing_shift_manager_http_client,
)
from models import Account
from parsers import (
    parse_account_login_form_data,
    parse_connect_authorize_form_data,
    parse_sign_in_oidc_form_data,
)

log = structlog.stdlib.get_logger()


def authenticate_unit(
        *,
        username: str,
        password: str,
        unit_uuid: UUID,
        country_code: str,
) -> dict[str, str]:
    with (
        bound_contextvars(username=username, unit_uuid=unit_uuid),
        closing_auth_http_client() as auth_http_client,
        closing_shift_manager_http_client(
            country_code=country_code,
        ) as shift_manager_http_client
    ):
        program = DodoConnection(
            auth_http_client=auth_http_client,
            shift_manager_http_client=shift_manager_http_client,
        )
        connect_authorize_form_html = program.go_to_shift_manager_domain()
        connect_authorize_form_data = parse_connect_authorize_form_data(
            connect_authorize_form_html=connect_authorize_form_html,
        )
        log.debug('Authorization: parsed connect authorize form data')

        account_login_form_html = program.send_connect_authorize_form_data(
            connect_authorize_form_data=connect_authorize_form_data,
        )

        account_login_form_data = parse_account_login_form_data(
            account_login_form_html=account_login_form_html,
            username=username,
            password=password,
            country_code=country_code,
        )
        log.debug('Authorization: parsed login form data')

        sign_in_oidc_form_html = program.send_account_login_form_data(
            account_login_form_data=account_login_form_data,
        )
        sign_in_oidc_form_data = parse_sign_in_oidc_form_data(
            sign_in_oidc_form_html=sign_in_oidc_form_html,
        )
        log.debug('Authorization: parsed sign in oidc form data')

        program.send_sign_in_oidc_form_data(sign_in_oidc_form_data,
                                            auth_http_client.cookies)
        log.debug('Authorization: sent sign in oidc form data')

        log.debug(shift_manager_http_client.cookies)

        program.send_select_role_form_data(unit_uuid)
        log.debug('Authorization: parsed select role form data')

        return dict(shift_manager_http_client.cookies)


def authenticate(
        account: Account,
        country_code: str,
):
    for unit in account.units:
        session = (
            authenticate_unit(
                username=account.username,
                password=account.password.get_secret_value(),
                unit_uuid=unit.uuid,
                country_code=country_code,
            )
        )
        httpx.patch('http://95.163.236.39/api/auth/auth/cookies/', json={
            'account_name': unit.account_name,
            'cookies': session,
        })


def main() -> None:
    accounts = load_accounts()
    for account in accounts:
        authenticate(
            account=account,
            country_code='ru',
        )


if __name__ == '__main__':
    main()
