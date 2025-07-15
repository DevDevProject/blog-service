import os
from typing import List
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import redis

from db.database import get_db
from models.Blog import Blog
load_dotenv()

REDIS_URL = os.getenv("REDIS_SERVER")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

redis_client = redis.Redis(
    host=REDIS_URL,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)

def increase_blog_score(blog_id: int):
    redis_client.zincrby("popular:blog", 1, str(blog_id))
    
def get_popular_blog_ids(limit: int = 10) -> List[int]:
    ids = redis_client.zrevrange("popular:blog", 0, limit - 1)
    return [int(i) for i in ids]

def get_popular_blogs(db: Session, ids: List[int]) -> List[Blog]:
    if not ids:
        return []

    blogs = (
        db.query(Blog)
            .join(Blog.company)
            .filter(Blog.id.in_(ids))
            .all()
    )

    id_to_blog = {c.id: c for c in blogs}
    return [id_to_blog[i] for i in ids if i in id_to_blog]

router = APIRouter()

@router.get("/popular")
def popular_companies(db: Session = Depends(get_db)):
    popular_ids = get_popular_blog_ids()
    blogs = get_popular_blogs(db, popular_ids)

    return [
        {
            "id": b.id,
            "title": b.title,
            "url": b.url,
            "company": b.company.name if b.company else None,
        }
        for b in blogs
    ]

@router.post("/popular")
def increase_popular_count(id: int):
    increase_blog_score(id)