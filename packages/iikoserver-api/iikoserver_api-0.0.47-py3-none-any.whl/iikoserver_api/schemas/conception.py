from typing import Optional

from pydantic import BaseModel


class Conception(BaseModel):
    id: str
    name: Optional[str] = None
    code: Optional[str] = None

