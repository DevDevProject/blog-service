from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.Base import Base

class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    image = Column(String(255))
    
    blogs = relationship("TechBlog", back_populates="company")