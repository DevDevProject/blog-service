from fastapi import APIRouter, Depends, Query, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session, selectinload
from typing import List, Optional
from schemas.request import CreateBlog
from schemas.response import BlogOut, BlogResponse, CompanyOut
from models.Blog import Blog
from models.Category import Category
from models.Company import Company
from crud.blog import create_blog
from db.database import get_db

router = APIRouter(prefix="/api/blog", tags=["Blog"])

@router.post("/add")
def add_blog(blog: CreateBlog, db: Session = Depends(get_db)):
    return create_blog(blog, db)

@router.post("/blogs")
def save_blogs(background_tasks: BackgroundTasks, blogs: List[CreateBlog], db: Session = Depends(get_db)):
    for blog in blogs:
        create_blog(blog, db, background_tasks)
    return {"status": "ok"}

@router.get("/blogs", response_model=BlogResponse)
def get_blogs(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit

    query = db.query(Blog).options(
        selectinload(Blog.company),
        selectinload(Blog.category)
    )

    if category and category.strip().lower() != 'all':
        query = query.join(Blog.category).filter(Category.name == category)

    if search:
        query = query.filter(
            (Blog.title.ilike(f"%{search}%")) |
            (Blog.description.ilike(f"%{search}%"))
        )

    total_count = query.count()
    blogs = query.offset(skip).limit(limit).all()

    result = [
        BlogOut(
            id=blog.id,
            title=blog.title,
            description=blog.description,
            url=blog.url,
            thumbnail=blog.thumbnail,
            create_date=blog.create_date,
            company=CompanyOut.from_orm(blog.company),
            category=blog.category.name if blog.category else None
        )
        for blog in blogs
    ]

    return BlogResponse(total_count=total_count, blogs=result)

@router.get("/urls")
def get_blogs(
    db: Session = Depends(get_db)
):
    urls = db.query(Blog.url).all()
    return [url[0] for url in urls]

@router.get("/{companyName}/blogs")
def get_company_blogs(
    companyName: str,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.name == companyName).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    offset = (page - 1) * limit
    
    total_count = (
        db.query(Blog)
        .filter(Blog.company_id == company.id)
        .count()
    )
    
    blogs = (db.query(Blog)
        .filter(Blog.company_id == company.id)
        .order_by(Blog.create_date.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    
    result = [
        BlogOut(
            id=blog.id,
            title=blog.title,
            description=blog.description,
            url=blog.url,
            thumbnail=blog.thumbnail,
            create_date=blog.create_date,
            company=CompanyOut.from_orm(blog.company),
            category=blog.category.name if blog.category else None
        )
        for blog in blogs
    ]
    
    return BlogResponse(total_count=total_count, blogs=result)