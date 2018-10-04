from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from . import util
from .model import *
bp = Blueprint("views", __name__)


@bp.route("/")
def index():
    genres = Genre.query.order_by(Genre.genre_name).all()
    # movies = Movie.query.order_by(Movie.title).all()
    # actors = Actor.query.order_by(Actor.name).all()
    # return render_template("home/index.html", genres=genres, movies=movies, actors=actors)
    return render_template("home/index.html", genres=genres)


@bp.route("/autocomplete", methods=["GET"])
def autocomplete():
    autocomplete = [movie.title for movie in Movie.query.all()]
    autocomplete += [actor.name for actor in Actor.query.all()]
    return jsonify(json_list=autocomplete)


###########
#  MOVIE  #
###########
@bp.route("/title/<item_id>")
def profile_movie(item_id):
    query = Movie.query.filter_by(title_id=item_id).first_or_404()
    formatted_genres = ", ".join([genre.genre_name for genre in query.genres])
    return render_template("title/profile.html", profile=query, genres=formatted_genres)


@bp.route("/title/create", methods=["POST", "GET"])
def create_movie():
    if request.method == "POST":
        title = request.form["title"]
        year = request.form["year"]
        cast = request.form["cast"].split(", ")
        genres = request.form["genres"].split(", ")
        item_id = util.add_to_movie_table(title, year, cast, genres)
        return redirect(url_for("views.profile_movie", item_id=item_id))

    return render_template("/title/create.html")


@bp.route("/title/<item_id>/edit", methods=["POST", "GET"])
def edit_movie(item_id):
    if request.method == "POST":
        title = request.form["title"]
        year = request.form["year"]
        cast = request.form["cast"].split(", ")
        genres = request.form["genres"].split(", ")
        util.save_to_movie_table(item_id, title, year, cast, genres)
        return redirect(url_for("views.profile_movie", item_id=item_id))

    query = Movie.query.filter_by(title_id=item_id).first_or_404()
    formatted_cast = ", ".join([actor.name for actor in query.cast])
    formatted_genres = ", ".join([genre.genre_name for genre in query.genres])
    return render_template("title/edit.html", profile=query, cast=formatted_cast, genres=formatted_genres)


@bp.route("/title/<item_id>/delete", methods=["POST", "GET"])
def delete_movie(item_id):
    util.remove_from_movie_table(item_id)
    return redirect(url_for("views.index"))


#########
# ACTOR #
#########
@bp.route("/name/<item_id>")
def profile_actor(item_id):
    query = Actor.query.filter_by(name_id=item_id).first_or_404()
    genre = util.get_actor_genre(query.genres)

    all_genres = []
    all_quantities = []
    for actor_genre in query.genres:
        all_genres.append(str(actor_genre.genre.genre_name))
        all_quantities.append(actor_genre.quantity)

    genre_data = str({"genres": all_genres, "quantities": all_quantities}).replace("'", "\"")
    return render_template("name/profile.html", profile=query, genre=genre, chart_data=genre_data)


@bp.route("/name/create", methods=["POST", "GET"])
def create_actor():
    if request.method == "POST":
        name = request.form["name"]
        filmography = request.form["filmography"].split(", ")
        item_id = util.add_to_actor_table(name, filmography)
        return redirect(url_for("views.profile_actor", item_id=item_id))

    return render_template("/name/create.html")


@bp.route("/name/<item_id>/edit", methods=["POST", "GET"])
def edit_actor(item_id):
    if request.method == "POST":
        name = request.form["name"]
        filmography = request.form["filmography"].split(", ")
        util.save_to_actor_table(item_id, name, filmography)
        return redirect(url_for("views.profile_actor", item_id=item_id))

    query = Actor.query.filter_by(name_id=item_id).first_or_404()
    formatted_filmography = ", ".join([movie.title for movie in query.filmography])
    return render_template("name/edit.html", profile=query, filmography=formatted_filmography)


@bp.route("/name/<item_id>/delete", methods=["POST", "GET"])
def delete_actor(item_id):
    util.remove_from_actor_table(item_id)
    return redirect(url_for("views.index"))
