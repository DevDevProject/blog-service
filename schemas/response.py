# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from typing import List

class CategoryOut(BaseModel):
    name: str

    class Config:
        from_attributes = True

class CompanyOut(BaseModel):
    name: str
    image: Optional[str]

    class Config:
        from_attributes = True

class BlogOut(BaseModel):
    id: int
    title: str
    description: str
    url: str
    thumbnail: str
    create_date: datetime
    company: CompanyOut
    category: Optional[str] = None

    class Config:
        from_attributes = True
        
class BlogResponse(BaseModel):
    blogs: List[BlogOut]
    total_count: int
