from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TIMESTAMP, Integer

Base = declarative_base()


class Article(Base):
    __tablename__ = 'articles'

    aid = Column(String, primary_key=True)
    oid = Column(Integer)
    title = Column(String)
    time = Column(TIMESTAMP(timezone=True))
    contents = Column(String)
