from datetime import datetime
from enum import StrEnum, auto
from typing import Optional

from pydantic import BaseModel


class ImplementationActItemTypeEnum(StrEnum):
    INCOMING = auto()
    OUTGOING = auto()


class ImplementationActItem(BaseModel):
    type: Optional[ImplementationActItemTypeEnum] = None
    sum: Optional[float] = None
    amount: Optional[float] = None
    store: Optional[str] = None
    account: Optional[str] = None
    product: Optional[str] = None


class ImplementationAct(BaseModel):
    id: str
    num: Optional[str] = None
    date: Optional[datetime] = None
    store: Optional[str] = None
    account: Optional[str] = None
    conception_code: Optional[str] = None
    items: list[ImplementationActItem] = []

