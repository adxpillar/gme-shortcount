from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GMEWiki(Base):
    __tablename__ = "gmewiki"
    datetime_checked = Column(TIMESTAMP(timezone=False), nullable=False, default=datetime.now())
    page_name = Column(String)
    word_count = Column (Integer)
