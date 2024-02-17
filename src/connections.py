from uuid import UUID

from models import (
    AccountLoginFormData,
    AuthHttpClient,
    ConnectAuthorizeFormData,
    ShiftManagerHttpClient,
    SignInOidcFormData,
)

__all__ = ('DodoConnection',)


class DodoConnection:

    def __init__(
            self,
            auth_http_client: AuthHttpClient,
            shift_manager_http_client: ShiftManagerHttpClient,
    ):
        self.auth_http_client = auth_http_client
        self.shift_manager_http_client = shift_manager_http_client

    def go_to_shift_manager_domain(self) -> str:
        response = self.shift_manager_http_client.get(
            url='/Infrastructure/Authenticate/Oidc'
        )
        return response.text

    def send_connect_authorize_form_data(
            self,
            connect_authorize_form_data: ConnectAuthorizeFormData,
    ) -> str:
        request_data = connect_authorize_form_data.model_dump()
        response = self.auth_http_client.post(
            url='/connect/authorize',
            data=request_data,
        )
        return response.text

    def send_account_login_form_data(
            self,
            account_login_form_data: AccountLoginFormData,
    ) -> str:
        request_data = account_login_form_data.model_dump()
        response = self.auth_http_client.post(
            url='/account/login',
            data=request_data,
        )
        return response.text

    def send_sign_in_oidc_form_data(
            self,
            sign_in_oidc_form_data: SignInOidcFormData,
    ) -> None:
        request_data = sign_in_oidc_form_data.model_dump()
        self.shift_manager_http_client.post(
            url='/signin-oidc',
            data=request_data,
        )

    def send_select_role_form_data(self, department_uuid: UUID) -> None:
        request_data = {
            'departmentId': department_uuid.hex,
            'role': 'ShiftManager',
        }
        self.shift_manager_http_client.post(
            url='/Infrastructure/Authenticate/SetRole',
            data=request_data,
        )
