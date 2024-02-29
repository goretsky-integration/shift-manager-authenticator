from pydantic import BaseModel

__all__ = ('SignInOidcFormData',)


class SignInOidcFormData(BaseModel):
    code: str
    scope: str
    state: str
    session_state: str
