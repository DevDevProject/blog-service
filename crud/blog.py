from sqlalchemy.orm import Session
from models.Blog import Blog
from models.Company import Company
from models.Category import Category
from schemas.request import CreateBlog
from kafka.producer import send_company_update
import asyncio
from db.database import get_db
from fastapi import BackgroundTasks

def create_blog(blog: CreateBlog, db: Session, background_tasks: BackgroundTasks):
    
    company = db.query(Company).filter(Company.name == blog.company_name).first()
    if not company:
        return {"error": "회사 없음"}
    
    new_blog = Blog(
        title=blog.title,
        url=blog.url,
        description=blog.description,
        thumbnail=blog.thumbnail,
        create_date=blog.create_date,
        company_id=company.id,
        category_id=None
    )
    db.add(new_blog)
    db.commit()
    
    print("✅ 저장 성공:", new_blog.id)
    background_tasks.add_task(send_company_update, blog.company_name)
    
    return {"status": "ok"}
