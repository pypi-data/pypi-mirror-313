from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class IncomingServiceItem(BaseModel):
    num: Optional[str] = None
    product: Optional[str] = None
    account: Optional[str] = None
    amount: Optional[float] = None
    sum: Optional[float] = None


class IncomingService(BaseModel):
    id: str
    date: Optional[datetime] = None
    num: Optional[str] = None
    account: Optional[str] = None
    counterparty: Optional[str] = None
    conception_code: Optional[str] = None
    items: list[IncomingServiceItem] = []

