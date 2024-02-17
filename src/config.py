import pathlib

from pydantic import TypeAdapter

from models import Account

__all__ = ('load_accounts',)


def load_accounts() -> list[Account]:
    accounts_file_path = pathlib.Path(__file__).parent.parent / 'accounts.json'
    accounts_json = accounts_file_path.read_text(encoding='utf-8')
    type_adapter = TypeAdapter(list[Account])
    return type_adapter.validate_json(accounts_json)
