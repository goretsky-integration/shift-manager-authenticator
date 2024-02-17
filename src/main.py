from uuid import UUID

from config import load_accounts
from connections import DodoConnection
from http_clients import (
    closing_auth_http_client,
    closing_shift_manager_http_client,
)
from models import (
    Account,
)
from parsers import (
    parse_account_login_form_data,
    parse_connect_authorize_form_data, parse_sign_in_oidc_form_data,
)


def authenticate_unit(
        *,
        username: str,
        password: str,
        unit_uuid: UUID,
        country_code: str,
) -> dict[str, str]:
    with closing_auth_http_client() as auth_http_client:
        with closing_shift_manager_http_client(
                country_code=country_code,
        ) as shift_manager_http_client:
            program = DodoConnection(
                auth_http_client=auth_http_client,
                shift_manager_http_client=shift_manager_http_client,
            )
            connect_authorize_form_html = program.go_to_shift_manager_domain()
            connect_authorize_form_data = parse_connect_authorize_form_data(
                connect_authorize_form_html=connect_authorize_form_html,
            )
            account_login_form_html = program.send_connect_authorize_form_data(
                connect_authorize_form_data=connect_authorize_form_data,
            )
            account_login_form_data = parse_account_login_form_data(
                account_login_form_html=account_login_form_html,
                username=username,
                password=password,
                country_code=country_code,
            )
            sign_in_oidc_form_html = program.send_account_login_form_data(
                account_login_form_data=account_login_form_data,
            )
            sign_in_oidc_form_data = parse_sign_in_oidc_form_data(
                sign_in_oidc_form_html=sign_in_oidc_form_html,
            )
            program.send_sign_in_oidc_form_data(sign_in_oidc_form_data)
            program.send_select_role_form_data(unit_uuid)

            return dict(shift_manager_http_client.cookies)


def authenticate(
        account: Account,
        country_code: str,
):
    for unit_uuid in account.unit_uuids:
        print(
            authenticate_unit(
                username=account.username,
                password=account.password.get_secret_value(),
                unit_uuid=unit_uuid,
                country_code=country_code,
            )
        )


def main() -> None:
    accounts = load_accounts()
    for account in accounts:
        authenticate(
            account=account,
            country_code='ru',
        )
