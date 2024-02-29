from uuid import UUID

import structlog.stdlib
from structlog.contextvars import bound_contextvars

from models import (
    AccountLoginFormData,
    AuthHttpClient,
    ConnectAuthorizeFormData,
    ShiftManagerHttpClient,
    SignInOidcFormData,
)

__all__ = ('DodoConnection',)

log = structlog.stdlib.get_logger('connection')


class DodoConnection:

    def __init__(
            self,
            auth_http_client: AuthHttpClient,
            shift_manager_http_client: ShiftManagerHttpClient,
    ):
        self.auth_http_client = auth_http_client
        self.shift_manager_http_client = shift_manager_http_client

    def go_to_shift_manager_domain(self) -> str:
        log.debug('1. Going to shift manager domain: sending')
        response = self.shift_manager_http_client.get(
            url='/Infrastructure/Authenticate/Oidc'
        )
        log.debug(
            '1. Going to shift manager domain: received',
            status=response.status_code,
        )
        return response.text

    def send_connect_authorize_form_data(
            self,
            connect_authorize_form_data: ConnectAuthorizeFormData,
    ) -> str:
        request_data = connect_authorize_form_data.model_dump()

        with bound_contextvars(request_data=request_data):
            log.debug('2. Connect authorize form data: sending')
            response = self.auth_http_client.post(
                url='/connect/authorize',
                data=request_data,
            )
            log.debug(
                '2. Connect authorize form data: received',
                status=response.status_code,
            )
        return response.text

    def send_account_login_form_data(
            self,
            account_login_form_data: AccountLoginFormData,
    ) -> str:
        request_data = {
            'ReturnUrl': account_login_form_data.return_url,
            'Username': account_login_form_data.username,
            'Password': account_login_form_data.password,
            'TenantName': account_login_form_data.tenant_name,
            'CountryCode': account_login_form_data.country_code,
            'authMethod': account_login_form_data.auth_method,
            '__RequestVerificationToken': account_login_form_data.request_verification_token,
            'RememberLogin': account_login_form_data.remember_login,
        }
        with bound_contextvars(request_data=request_data):
            log.debug('3. Account login form data: sending')
            response = self.auth_http_client.post(
                url='/account/login',
                data=request_data,
            )
            log.debug(
                '3. Account login form data: received',
                status=response.status_code,
            )
        return response.text

    def send_sign_in_oidc_form_data(
            self,
            sign_in_oidc_form_data: SignInOidcFormData,
            cookies,
    ) -> None:
        request_data = {
            'code': sign_in_oidc_form_data.code,
            'scope': sign_in_oidc_form_data.scope,
            'state': sign_in_oidc_form_data.state,
            'session_state': sign_in_oidc_form_data.session_state,
        }
        with bound_contextvars(request_data=request_data):
            log.debug('4. Sign in OIDC form data: sending')
            response = self.shift_manager_http_client.post(
                url='/signin-oidc',
                data=request_data,
                cookies=cookies,
            )
            log.debug(
                '4. Sign in OIDC form data: received',
                status=response.status_code,
            )

    def send_select_role_form_data(self, department_uuid: UUID) -> None:
        request_data = {
            'departmentId': department_uuid.hex,
            'role': 'ShiftManager',
        }
        with bound_contextvars(request_data=request_data):
            log.debug('5. Select role form data: sending')
            response = self.shift_manager_http_client.post(
                url='/Infrastructure/Authenticate/SetRole',
                json=request_data,
            )
            log.debug(
                '5. Select role form data: received',
                status=response.status_code,
            )
