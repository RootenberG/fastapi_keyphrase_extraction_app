from src.app.db import db


class Text(db.Model):
    __tablename__ = "texts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
