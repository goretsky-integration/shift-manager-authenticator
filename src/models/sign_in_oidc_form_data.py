from pydantic import BaseModel

__all__ = ('SignInOidcFormData',)


class SignInOidcFormData(BaseModel):
    code: str | None
    scope: str | None
    state: str | None
    session_state: str | None
