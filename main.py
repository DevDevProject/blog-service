from fastapi import FastAPI, Depends, UploadFile, File, Form
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.responses import JSONResponse
import shutil
import os
# from models.TechBlog import TechBlog, Company
from models.Company import Company
from models.Category import Category
from models.TechBlog import TechBlog
from pydantic import BaseModel
from sqlalchemy.orm import Session, selectinload
from fastapi import Query
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger
from schemas.response import BlogOut
from typing import List
from models import Base
from schemas.response import CompanyOut
from schemas.response import BlogResponse

from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

SQLALCHEMY_DATABASE_URL = os.environ["DB_URL"]

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 또는 ["*"] 개발 중일 때
    allow_credentials=True,
    allow_methods=["*"],  # ["GET", "POST", "OPTIONS", "PUT", "DELETE"] 등
    allow_headers=["*"],
)

class CreateBlog(BaseModel):
    title: str
    description: str
    company_name: str
    url: str
    thumbnail: str
    create_date: str
    category: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/blog/add")
def create_blog(
    data: CreateBlog,
    db: Session = Depends(get_db)
):
    
    company = db.query(Company).filter(Company.name == data.company_name).first()
    if company is None:
        return {"error": "회사 없음"}
    
    category = db.query(Category).filter(Category.name == data.category).first()
    if company is None:
        return {"error": "카테고리 없음"}
    
    blog = TechBlog(
        title=data.title,
        url=data.url,
        description=data.description,
        thumbnail=data.thumbnail,
        create_date = data.create_date,
        company_id = company.id,
        category_id = category.id
    )
    
    db.add(blog)
    db.commit()
    
    return {
        "status": "ok"
    }
    
@app.get("/api/blog/blogs", response_model=BlogResponse)
def get_blogs(
        page: int = Query(1, ge = 1),
        limit: int = Query(10, ge=1),
        search: Optional[str] = Query(None),
        category: Optional[str] = Query(None),
        db: Session = Depends(get_db)
    ):
    skip = (page - 1) * limit

    query = db.query(TechBlog).options(
        selectinload(TechBlog.company),
        selectinload(TechBlog.category)
    )
    
    if category and category.strip().lower() == 'all':
        category = ''
    
    if search:
        query = query.filter(
            (TechBlog.title.ilike(f"%{search}%")) |
            (TechBlog.description.ilike(f"%{search}%"))
        )
        
    if category:
        query = query.join(TechBlog.category).filter(Category.name == category)

    total = query.count()
    blogs = query.offset(skip).limit(limit).all()

    blogs = [
        BlogOut(
            id=blog.id,
            title=blog.title,
            description=blog.description,
            url=blog.url,
            thumbnail=blog.thumbnail,
            create_date=blog.create_date,
            company=CompanyOut.from_orm(blog.company),
            category=blog.category.name
        )
        for blog in blogs
    ]

    return {
        "total": total,
        "blogs": blogs
    }

    