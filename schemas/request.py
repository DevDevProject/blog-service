from typing import Optional
from pydantic import BaseModel
from datetime import date

class CreateBlog(BaseModel):
    title: str
    description: str
    company_name: Optional[str] = None
    url: str
    thumbnail: Optional[str] = None
    create_date: date
    category: Optional[str] = None