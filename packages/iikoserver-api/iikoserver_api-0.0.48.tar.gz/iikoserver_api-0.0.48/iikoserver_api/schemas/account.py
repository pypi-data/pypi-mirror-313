from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_pascal


def account_alias_generator(string: str) -> str:
    return 'Account.' + to_pascal(string)


class Account(BaseModel):
    model_config = ConfigDict(alias_generator=account_alias_generator, use_enum_values=True)
    id: str
    name: Optional[str] = None


