from typing import Optional

from pydantic import BaseModel


class IncomingInvoiceItem(BaseModel):
    actual_amount: Optional[float] = None
    store: Optional[str] = None
    code: Optional[str] = None
    price: Optional[float] = None
    sum: Optional[float] = None
    vat_percent: Optional[float] = None
    vat_sum: Optional[float] = None
    discount_sum: Optional[float] = None
    amount_unit: Optional[str] = None
    num: Optional[int] = None
    product: Optional[str] = None
    product_article: Optional[str] = None
    amount: Optional[float] = None


class IncomingInvoice(BaseModel):
    id: str
    items: list[IncomingInvoiceItem] = []
    incoming_document_number: Optional[str] = None
    incoming_date: Optional[str] = None
    use_default_document_time: Optional[bool] = None
    due_date: Optional[str] = None
    supplier: Optional[str] = None
    default_store: Optional[str] = None
    document_number: Optional[str] = None
    invoice: Optional[str] = None
    comment: Optional[str] = None
    status: Optional[str] = None
    conception_code: Optional[str] = None
    conception: Optional[str] = None



