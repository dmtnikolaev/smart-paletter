from sqlalchemy.sql import func

from src import dependencies as deps

db = deps.db

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(1024), nullable=False)
    uploaded_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, path):
        self.path = path
