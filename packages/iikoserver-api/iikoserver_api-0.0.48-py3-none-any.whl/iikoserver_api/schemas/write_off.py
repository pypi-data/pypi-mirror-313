from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class WriteOffItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, use_enum_values=True)
    num: int
    product_id: Optional[str] = None
    product_size_id: Optional[str] = None
    amount_factor: Optional[float] = None
    amount: Optional[float] = None
    measure_unit_id: Optional[str] = None
    container_id: Optional[str] = None
    cost: Optional[float] = None


class WriteOff(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, use_enum_values=True)
    id: Optional[str]
    date_incoming: Optional[str] = None
    document_number: Optional[str] = None
    status: Optional[str] = None
    conception_id: Optional[str] = None
    comment: Optional[str] = None
    store_id: Optional[str] = None
    account_id: Optional[str] = None
    external_outgoing_invoice_id: Optional[str] = None
    external_production_document_id: Optional[str] = None
    items: list[WriteOffItem] = []

