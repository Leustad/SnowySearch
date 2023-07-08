from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.functions import func

from search.db.db import Base


# Define a model for the table you want to insert into
class News(Base):
    __tablename__ = "news"
    __table_args__ = {"schema": "snowy_search"}

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    article_insert_date = Column(DateTime, nullable=False, server_default=func.now())
    article_publish_date = Column(DateTime, nullable=False)
    text = Column(String, nullable=False)
    title_hash = Column(String, nullable=False, index=True, unique=True)
