from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.Base import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    
    blogs = relationship("TechBlog", back_populates="category")