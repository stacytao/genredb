from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('../instance/config.py')
db = SQLAlchemy(app)

casts = db.Table(
    'casts',
    db.Column('name_id', db.Integer, db.ForeignKey('actor.name_id')),
    db.Column('title_id', db.Integer, db.ForeignKey('tv_show.title_id'))
)


class Actor(db.Model):
    name_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    filmography = db.relationship(
        'TvShow',
        secondary=casts,
        backref=db.backref('cast', lazy='dynamic')
    )

    def __repr__(self):
        return '<Actor %r>' % self.name


class TvShow(db.Model):
    title_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<TvShow %r>' % self.title
