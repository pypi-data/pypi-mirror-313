from typing import Optional

from pydantic import BaseModel


class Employee(BaseModel):
    id: str
    code: Optional[str] = None
    name: Optional[str] = None
    login: Optional[str] = None
    phone: Optional[str] = None
    cell_phone: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    note: Optional[str] = None
    card_number: Optional[str] = None
    taxpayer_id_number: Optional[str] = None
    snils: Optional[str] = None
    preferred_department_code: Optional[str] = None
    deleted: Optional[bool] = None
    supplier: Optional[bool] = None
    employee: Optional[bool] = None
    client: Optional[bool] = None
    represents_store: Optional[bool] = None

