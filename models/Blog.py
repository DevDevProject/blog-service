from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from models.Base import Base


class Blog(Base):
    __tablename__ = "blog"

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(255))
    url = Column(String(255))
    description = Column(String(1000))
    thumbnail = Column(String(255))
    create_date = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text)
    
    company_id = Column(BigInteger, ForeignKey("company.id"))
    category_id = Column(BigInteger, ForeignKey("category.id"))
    
    company = relationship("Company", back_populates="blogs")
    category = relationship("Category", back_populates="blogs")