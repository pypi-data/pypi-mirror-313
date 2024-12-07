from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class NomenclatureGroup(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, use_enum_values=True)
    id: Optional[str]
    deleted: Optional[bool] = None
    name: Optional[str] = None
    description: Optional[str] = None
    num: Optional[str] = None
    code: Optional[str] = None
    parent: Optional[str] = None
    modifiers: Optional[list] = None
    tax_category: Optional[str] = None
    category: Optional[str] = None
    accounting_category: Optional[str] = None
    font_image_id: Optional[str] = None
    position: Optional[int] = None



