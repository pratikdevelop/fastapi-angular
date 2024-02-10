from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    id: Optional[int] = None
    todo_name: str
    todo_description: str 

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

