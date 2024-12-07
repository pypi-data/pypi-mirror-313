from enum import StrEnum, auto
from typing import Optional

from pydantic import BaseModel


class InventoryItemEnum(StrEnum):
    INCOMING = auto()
    OUTGOING = auto()


class InventoryItem(BaseModel):
    sum: Optional[float] = None
    type: Optional[InventoryItemEnum] = None
    account: Optional[str] = None


class Inventory(BaseModel):
    id: str
    store: Optional[str] = None
    num: Optional[str] = None
    date: Optional[str] = None
    incoming_sum: Optional[float] = None
    outgoing_sum: Optional[float] = None
    sum: Optional[float] = None
    items: list[InventoryItem] = []




