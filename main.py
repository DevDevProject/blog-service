from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import blog as blog_router
from api import popular_blog as popular_blog_router
from db.database import engine
from models import Base

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(blog_router.router)
app.include_router(popular_blog_router.router, prefix="/api/blog")