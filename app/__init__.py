from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from manage import session, publish

app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)

all_published = []

@app.route('/')
def hello_world():
    (topic, articles) = publish()
    if topic is not None:        
        all_published.append((topic, articles))
        # summary: article.summ
        # title: article.title
        # url: article.url
        data = {"clumps" : [{'title' : a1.title,
                             'image' : 'mudkip.png',
                             'url'   : a1.url,
                             'info'  : a1.summ,
                             'viewpoint1' : a2.url,
                             'viewpoint1blurb' : a2.title,
                             'viewpoint2' : a1.url,
                             'viewpoint2blurb' : a1.title
                             } for (t, [a1, a2]) in all_published]}
    return render_template('bootstrap_mainpage.html', data)

@app.route('/post/<topic>')
def show_topic_page(topic):
    # display the page for that topic
    pass

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.close()

import models

if __name__ == '__main__':
    app.run(host = ('0.0.0.0'))
