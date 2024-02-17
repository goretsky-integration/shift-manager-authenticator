from uuid import UUID

from pydantic import BaseModel, SecretStr

__all__ = ('Account',)


class Account(BaseModel):
    username: str
    password: SecretStr
    unit_uuids: list[UUID]
