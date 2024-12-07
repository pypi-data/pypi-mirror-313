from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ReturningInvoiceItem(BaseModel):
    num: str
    amount: Optional[float] = None
    product: Optional[str] = None
    sum: Optional[float] = None
    store: Optional[str] = None
    account: Optional[str] = None


class ReturningInvoice(BaseModel):
    id: str
    number: Optional[str] = None
    date: Optional[datetime] = None
    account: Optional[str] = None
    counterparty: Optional[str] = None
    conception_code: Optional[str] = None
    items: list[ReturningInvoiceItem] = []
