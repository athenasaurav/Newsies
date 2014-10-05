from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import newsiedb

app = Flask(__name__)
app.config.from_pyfile(config.py)
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return "Break time!"

@app.route('/post/<topic>')
def show_topic_page(topic):
    # display the page for that topic
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0')
