from typing import Optional

from pydantic import BaseModel


class OutgoingInvoiceItem(BaseModel):
    product_id: Optional[str] = None
    product_article: Optional[str] = None
    store_id: Optional[str] = None
    store_code: Optional[str] = None
    price: Optional[float] = None
    amount: Optional[float] = None
    sum: Optional[float] = None
    discount_sum: Optional[float] = None
    vat_percent: Optional[float] = None
    vat_sum: Optional[float] = None


class OutgoingInvoice(BaseModel):
    id: str
    document_number: Optional[str] = None
    date_incoming: Optional[str] = None
    use_default_document_time: Optional[bool] = None
    status: Optional[str] = None
    account_to_code: Optional[str] = None
    revenue_account_code: Optional[str] = None
    default_store_id: Optional[str] = None
    default_store_code: Optional[str] = None
    counteragent_id: Optional[str] = None
    counteragent_code: Optional[str] = None
    comment: Optional[str] = None
    conception_code: Optional[str] = None
    conception_id: Optional[str] = None
    items: list[OutgoingInvoiceItem] = []

