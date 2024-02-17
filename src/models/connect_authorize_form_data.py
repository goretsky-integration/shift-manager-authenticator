from pydantic import BaseModel

__all__ = ('ConnectAuthorizeFormData',)


class ConnectAuthorizeFormData(BaseModel):
    client_id: str | None
    redirect_uri: str | None
    response_type: str | None
    scope: str | None
    code_challenge: str | None
    code_challenge_method: str | None
    response_mode: str | None
    nonce: str | None
    state: str | None
