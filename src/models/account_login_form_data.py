from pydantic import BaseModel

__all__ = ('AccountLoginFormData',)


class AccountLoginFormData(BaseModel):
    return_url: str
    username: str
    password: str
    tenant_name: str
    country_code: str
    auth_method: str
    remember_login: bool
    request_verification_token: str
