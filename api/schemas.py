from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile

class ItemBase(BaseModel):
    id: Optional[int] = None
    todo_name: str 
    todo_description: str 
    todo_image: UploadFile

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

