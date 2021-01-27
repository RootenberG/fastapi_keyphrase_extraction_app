from src.app.db import db


class Word(db.Model):
    __tablename__ = "words"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text_id = db.Column(db.Integer, db.ForeignKey("texts.id"))
    word = db.Column(db.String(55), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    is_wiki_has = db.Column(db.Boolean)
    is_disambiguation = db.Column(db.Boolean, default=False)
