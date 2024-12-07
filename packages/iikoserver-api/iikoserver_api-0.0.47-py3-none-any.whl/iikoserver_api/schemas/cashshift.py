from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Cashshift(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, use_enum_values=True)
    id: Optional[str]
    session_number: Optional[int] = None
    fiscal_number: Optional[int] = None
    cash_reg_number: Optional[int] = None
    cash_reg_serial: Optional[str] = None
    open_date: Optional[str] = None
    close_date: Optional[str] = None
    accept_date: Optional[str] = None
    manager_id: Optional[str] = None
    responsible_user: Optional[str] = None
    session_start_cash: Optional[float] = None
    pay_orders: Optional[float] = None
    sum_writeoff_orders: Optional[float] = None
    sales_cash: Optional[float] = None
    sales_credit: Optional[float] = None
    sales_card: Optional[float] = None
    pay_in: Optional[float] = None
    pay_out: Optional[float] = None
    pay_income: Optional[float] = None
    cash_remain: Optional[float] = None
    cash_diff: Optional[float] = None
    session_status: Optional[str] = None
    conception: Optional[str] = None
    point_of_sale: Optional[str] = None


class OlapCashShift(BaseModel):
    id: str
    session_number: Optional[int] = None
    cash_shift_name: Optional[str] = None
    close_date: Optional[datetime] = None
    amount: Optional[float] = None


class OlapCashShiftV2(BaseModel):
    id: str
    session_number: Optional[str] = None
    cash_shift_name: Optional[str] = None
    cash_shift_number: Optional[str] = None
    cash_shift_serial: Optional[str] = None
    cash_shitf_id: Optional[str] = None
    close_date: Optional[datetime] = None
    amount: Optional[float] = None
