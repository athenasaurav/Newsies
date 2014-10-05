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
    sent_pos = Column(Real, nullable=True)
    sent_neg = Column(Float, nullable=True)

class Topic(Base):
    __tablename__ = "topic"

    id = Column(Integer, primary_key=True)
    topic_str = Column(String(100), nullable=False)

class ArticleToTopic(Base):
    __tablename__ = "article_to_topic"
    
    article_id = Column(Integer, ForeignKey("article.id"), primary_key=True)
    topic_id = Column(Integer, ForeginKey("topic.id"), primary_key=True)
    weight = Column(Float, nullable=False)

    article = relationship("Article", backref="article_topics")
    topic = relationship("Topic", backref="topic_articles")

engine = create_engine("sqlite:///newsie_data.db")

Base.metadata.create_all(engine)
