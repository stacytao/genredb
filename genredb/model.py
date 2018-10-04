from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('../instance/config.py')
db = SQLAlchemy(app)

casts = db.Table(
    'casts',
    db.Column('name_id', db.Integer, db.ForeignKey('actor.name_id')),
    db.Column('title_id', db.Integer, db.ForeignKey('movie.title_id'))
)

titles = db.Table(
    'titles',
    db.Column('title_id', db.Integer, db.ForeignKey('movie.title_id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.genre_id'))
)


class Movie(db.Model):
    title_id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.Unicode(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    genres = db.relationship(
        'Genre',
        secondary=titles,
        backref=db.backref('titles', lazy='dynamic')
    )

    def __init__(self, title, year):
        self.title = title
        self.year = year

    def __repr__(self):
        return '<Movie {} ({})>'.format(self.title, self.year)


class Actor(db.Model):
    name_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.Unicode(80), nullable=False)

    filmography = db.relationship(
        'Movie',
        secondary=casts,
        backref=db.backref('cast', lazy='dynamic')
    )

    genres = db.relationship(
        'ActorGenre',
        backref=db.backref('actor')
    )

    def __repr__(self):
        return '<Actor {}>'.format(self.name)


class Genre(db.Model):
    genre_id = db.Column(db.Integer, primary_key=True, unique=True)
    genre_name = db.Column(db.Unicode(80), nullable=False)

    def __repr__(self):
        return '<Genre {}>'.format(self.genre_name)


class ActorGenre(db.Model):
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.name_id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, genre, quantity):
        self.genre = genre
        self.quantity = quantity
    genre = db.relationship(Genre, lazy='joined')

    def __repr__(self):
        return '<ActorGenre {} in {} = {}>'.format(self.actor.name, self.genre.genre_name, self.quantity)
