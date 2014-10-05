from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from manage import session, publish

app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    (topic, articles) = publish()
    # summary: article.summ
    # title: article.title
    # url: article.url
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
