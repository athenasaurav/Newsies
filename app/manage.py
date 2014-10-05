from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import create_engine
import datetime

Base = declarative_base()
engine = create_engine("sqlite:///db_files/testdb.db", convert_unicode=True)

session = scoped_session(sessionmaker(autocommit = False, bind = engine))
Base.query = session.query_property()

def initdb():
    import models
    Base.metadata.create_all(bind = engine)

def write_db(entry):
    from models import Article
    date = entry["published_parsed"]
    new_article = Article(url = entry["link"], title = entry["title"],
        timestamp = datetime.datetime(date[0], date[1], date[2], date[3], date[4], date[5], date[6]),
        summ = entry["summary"])
    session.add(new_article)
    session.commit()

# article is the article url, topic_list contains (topic string, weight), 
# (pos, neg) is positive and negative sentiment
def addArticle(article, topic_list, (pos, neg)):
    from models import Article, Topic, ArticleToTopic
    new_article = Article(url = article, sent_pos = pos, sent_neg = neg)
    session.add(new_article)

    # TODO: check whether new_topic is already in the database
    for (new_topic, top_weight) in topic_list:
        cur_topic = session.query(Topic).filter_by(topic_str=new_topic).all()
        if len(cur_topic) == 0:
            topic_obj = Topic(topic_str = new_topic)
        else:
            topic_obj = cur_topic[0]
        new_article.article_topics.extend([
            ArticleToTopic(topic = topic_obj, weight = top_weight)
        ])
        session.add(topic_obj)
    session.commit()

# should another article be published
def publish():
    (topic, articleList) = chooseTopic()
    if topic != None:
        print topic.topic_str
    articles = chooseArticles(articleList)
    return (topic, articles)

# TODO: make this smarter by factoring in topic-article weights
# TODO: check whether an article was previously published
def chooseTopic():
    from models import Topic, ArticleToTopic, Article
    publishThresh = 2
    for topic in session.query(Topic).distinct():
        print topic
        articleList = session.query(ArticleToTopic).filter_by(topic_id=topic.id).all()
        if len(articleList) > publishThresh:
            return (topic, articleList)
    print "No topic selected"
    return (None, [])
  
# TODO: choose more than two articles, choose more intelligently
def chooseArticles(articleList):
    if len(articleList) == 0:
        return []
    maxPos = 0
    minNeg = 0
    posArticle = ""
    negArticle = ""

    for article in articleList:
        psent = article.sent_pos
        nsent = article.sent_neg
        pdiff = psent - maxPos
        ndiff = minNeg - nsent
        if maxPos < psent:
                maxPos = psent
                posArticle = article
        if minNeg > nsent:
            if pdiff > ndiff:
                maxPos = psent
                posArticle = article
            else:
                minNeg = nsent
                negArticle = article
    return [posArticle, negArticle]
            
