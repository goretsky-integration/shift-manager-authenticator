from pydantic import BaseModel, SecretStr

from models.units import Unit

__all__ = ('Account',)


class Account(BaseModel):
    username: str
    password: SecretStr
    units: list[Unit]
