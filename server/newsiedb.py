from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Article(Base):
    __tablename__ = "article"

    # define columns for article table
    id = Column(Integer, primary_key=True)
    url = Column(String(500), nullable=False)
    sent_pos = Column(Float, nullable=True)
    sent_neg = Column(Float, nullable=True)

    topics = relationship(
        "Topic",
        secondary = Table("article_topic", Base.metadata,
            Column("article_id", Integer, ForeignKey("article.id"), 
                primary_key = True),
            Column("topic_id", Integer, ForeginKey("topic.id"),
                primary_key = True)
        ),
    backref = "articles"
    )

class 

