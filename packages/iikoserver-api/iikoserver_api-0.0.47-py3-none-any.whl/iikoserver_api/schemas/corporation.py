from typing import Optional

from pydantic import BaseModel


class CorporationStore(BaseModel):
    id: Optional[str] = None
    parent_id: Optional[str] = None
    code: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None

