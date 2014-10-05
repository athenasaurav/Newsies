from config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path

db.create_all()
if not os.path.exists(SQLALCHEMY_DATABASE_URI):
    api.create(SQLALCHEMY_DATABASE_URI, 'database repository')
