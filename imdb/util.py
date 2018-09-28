import json
from .model import *


def init_db():
    db.create_all()
    with open('/Users/Stacy/Documents/Columbia/Junior Year/IMDb/imdb/movies.json') as f:
        data = json.load(f)
        for movie in data:
            title = movie["title"]
            year = movie["year"]
            cast = movie["cast"].split(", ")
            genres = movie["genre"].split(", ")
            add_to_movie_table(title, year, cast, genres)


def add_to_actor_genre(actor, genres):
    for genre in genres:
        # print(genre)
        item_actor_genre = ActorGenre.query.filter_by(actor_id=actor.name_id, genre_id=genre.genre_id).first()
        if item_actor_genre is None:
            item_actor_genre = ActorGenre(genre=genre, quantity=1)
            actor.genres.append(item_actor_genre)
        else:
            item_actor_genre.quantity += 1


# def remove_from_actor_genre(actor, genres):


def get_actor_genre(actor_genres):
    genre_list = []
    max_quantity = 0
    for actor_genre in actor_genres:
        if actor_genre.quantity > max_quantity:
            max_quantity = actor_genre.quantity
            genre_list = [actor_genre.genre.genre_name]
        elif actor_genre.quantity == max_quantity:
            genre_list.append(actor_genre.genre.genre_name)
    return ", ".join(genre_list)


###########
#  MOVIE  #
###########
def add_to_movie_table(item_title, item_year, item_cast, item_genres):
    # Check if already exists (prevent duplicates)
    existing = Movie.query.filter_by(title=item_title).filter_by(year=item_year).first()
    if existing is not None:
        save_to_movie_table(existing.title_id, item_year, item_title, item_cast, item_genres)
        return existing.title_id

    # Create new
    movie = Movie(title=item_title, year=int(item_year))
    db.session.add(movie)

    for genre_name in item_genres:
        genre = Genre.query.filter_by(genre_name=genre_name).first()
        if genre is None:
            genre = Genre(genre_name=genre_name)
            db.session.add(genre)
        movie.genres.append(genre)

    for actor_name in item_cast:
        actor = Actor.query.filter_by(name=actor_name).first()
        if actor is None:
            actor = Actor(name=actor_name)
            db.session.add(actor)
        movie.cast.append(actor)
        add_to_actor_genre(actor, movie.genres)

    db.session.commit()
    return movie.title_id


def save_to_movie_table(item_id, item_year, item_title, item_cast, item_genres):
    movie = Movie.query.filter_by(title_id=item_id).first()
    movie.title = item_title
    movie.year = int(item_year)

    for actor in movie.cast:
        if actor.name not in item_cast:
            movie.cast.remove(actor)

    for genre_name in item_genres:
        genre = Genre.query.filter_by(genre_name=genre_name).first()
        if genre is None:
            genre = Genre(genre_name=genre_name)
            db.session.add(genre)
            movie.genres.append(genre)
        elif genre not in movie.genres:
            movie.genres.append(genre)

    for genre in movie.genres:
        if genre.genre_name not in item_genres:
            movie.genres.remove(genre)

    for actor_name in item_cast:
        actor = Actor.query.filter_by(name=actor_name).first()
        if actor is None:
            actor = Actor(name=actor_name)
            db.session.add(actor)
            movie.cast.append(actor)
        elif actor not in movie.cast:
            movie.cast.append(actor)

    db.session.commit()


def remove_from_movie_table(item_id):
    movie = Movie.query.filter_by(title_id=item_id).first_or_404()
    db.session.delete(movie)
    db.session.commit()


#########
# ACTOR #
#########
def add_to_actor_table(item_name, item_filmography):
    actor = Actor(name=item_name)
    db.session.add(actor)

    for movie_title in item_filmography:
        movie = Movie.query.filter_by(title=movie_title).first()
        if movie is None:
            movie = Movie(title=movie_title)
            db.session.add(movie)
        actor.filmography.append(movie)

    db.session.commit()
    return actor.name_id


def save_to_actor_table(item_id, item_name, item_filmography):
    actor = Actor.query.filter_by(name_id=item_id).first()
    actor.name = item_name

    for movie_title in item_filmography:
        movie = Movie.query.filter_by(title=movie_title).first()
        if movie is None:
            movie = Movie(title=movie_title)
            db.session.add(movie)
            actor.filmography.append(movie)
        elif movie not in actor.filmography:
            actor.filmography.append(movie)

    for movie in actor.filmography:
        if movie.title not in item_filmography:
            actor.filmography.remove(movie)

    db.session.commit()


def remove_from_actor_table(item_id):
    actor = Actor.query.filter_by(name_id=item_id).first_or_404()
    db.session.delete(actor)
    db.session.commit()
