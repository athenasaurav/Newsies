from manage import Base
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

class Article(Base):
    __tablename__ = "article"
    __table_args__ = {'sqlite_autoincrement': True}

    # define columns for article table
    id = Column(Integer, primary_key=True)
    url = Column(String(500), nullable=False)
    sent_pos = Column(Float, nullable=True)
    sent_neg = Column(Float, nullable=True)
    published = Column(Boolean, nullable=True)
    title = Column(String(500), nullable=True)
    summ = Column(String(2000), nullable=True)
    timestamp = Column(DateTime, nullable=True)

class Topic(Base):
    __tablename__ = "topic"
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    topic_str = Column(String(100), nullable=False)

class ArticleToTopic(Base):
    __tablename__ = "article_to_topic"
    
    article_id = Column(Integer, ForeignKey("article.id"), primary_key=True)
    topic_id = Column(Integer, ForeignKey("topic.id"), primary_key=True)
    weight = Column(Float, nullable=False)

    article = relationship("Article", backref="article_topics")
    topic = relationship("Topic", backref="topic_articles")

