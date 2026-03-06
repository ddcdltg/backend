from pydantic import BaseModel
from typing import List, Optional

class DataTableOut(BaseModel):
    draw: int
    recordsTotal: int
    recordsFiltered: int
    data: List[StatusOut]

class StatusOut(BaseModel):
    status_id: int   
    name: str       
    description: Optional[str] = None 
    permissions: Optional[list[str]] = None 

    class Config:
        from_attributes = True
        extra = "forbid"