from flask import Blueprint, g, jsonify, render_template, request, redirect, session, url_for
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from . import util
from .model import *
bp = Blueprint("views", __name__)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(user_id=user_id).first()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("views.login_user", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@bp.route("/")
def index():
    genres = Genre.query.order_by(Genre.genre_name).all()
    # movies = Movie.query.order_by(Movie.title).all()
    # actors = Actor.query.order_by(Actor.name).all()
    # return render_template("home/index.html", genres=genres, movies=movies, actors=actors)
    return render_template("home/index.html", genres=genres)


@bp.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('home/404.html'), 404


@bp.route("/autocomplete", methods=["GET"])
def autocomplete():
    # autocomplete = [movie.title for movie in Movie.query.all()]
    # autocomplete += [actor.name for actor in Actor.query.all()]
    return jsonify(json_list=[actor.name for actor in Actor.query.all()])


@bp.route("/search/<item_query>")
def search_query(item_query):
    query = Actor.query.filter_by(name=item_query).first_or_404()
    item_id = query.name_id
    return redirect(url_for("views.profile_actor", item_id=item_id))


###########
#  USERS  #
###########
@bp.route("/register", methods=["POST", "GET"])
def register_user():
    registration_error = False
    errors = {
        "username": None,
        "password": None
    }

    if request.method == "POST" and "form-button" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]

        user_exists = User.query.filter_by(username=username).count() > 0
        if user_exists is True:
            registration_error = True
            errors["username"] = "Username already exists. Please choose another one."

        if registration_error:
            return render_template("/user/register.html", error=errors)

        util.add_to_user_table(username, generate_password_hash(password), name)
        return redirect(url_for("views.login_user"))

    return render_template("/user/register.html")


@bp.route("/login", methods=["POST", "GET"])
def login_user():
    login_error = False
    errors = {
        "username": None,
        "password": "Hello"
    }

    if request.method == "POST" and "form-button" in request.form:
        username = request.form["username"]
        password = request.form["password"]

        users = User.query.filter_by(username=username)
        user = None
        if users.count() == 0:
            login_error = True
            errors["username"] = "Username doesn't exist. Please check your spelling."
        else:
            user = users.first()
            if not check_password_hash(user.password, password):
                login_error = True
                errors["password"] = "Incorrect password. Please try again."

        if login_error:
            return render_template("/user/login.html", error=errors)

        session.clear()
        session["user_id"] = user.user_id
        session["user_name"] = user.user_name
        return redirect(request.args.get("next") or url_for("views.index"))

    return render_template("/user/login.html")


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.index'))


###########
#  MOVIE  #
###########
@bp.route("/title/<item_id>")
def profile_movie(item_id):
    query = Movie.query.filter_by(title_id=item_id).first_or_404()
    formatted_genres = ", ".join([genre.genre_name for genre in query.genres])
    return render_template("title/profile.html", profile=query, genres=formatted_genres)


@bp.route("/title/create", methods=["POST", "GET"])
@login_required
def create_movie():
    if request.method == "POST" and "form-button" in request.form:
        title = request.form["title"]
        year = request.form["year"]
        cast = request.form["cast"].split(", ")
        genres = request.form["genres"].split(", ")
        item_id = util.add_to_movie_table(title, year, cast, genres)
        return redirect(url_for("views.profile_movie", item_id=item_id))

    return render_template("/title/create.html")


@bp.route("/title/<item_id>/edit", methods=["POST", "GET"])
@login_required
def edit_movie(item_id):
    if request.method == "POST" and "form-button" in request.form:
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


@bp.route("/title/<item_id>/delete")
@login_required
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
@login_required
def create_actor():
    if request.method == "POST" and "form-button" in request.form:
        name = request.form["name"]
        filmography = request.form["filmography"].split(", ")
        item_id = util.add_to_actor_table(name, filmography)
        return redirect(url_for("views.profile_actor", item_id=item_id))

    return render_template("/name/create.html")


@bp.route("/name/<item_id>/edit", methods=["POST", "GET"])
@login_required
def edit_actor(item_id):
    if request.method == "POST" and "form-button" in request.form:
        name = request.form["name"]
        filmography = request.form["filmography"].split(", ")
        util.save_to_actor_table(item_id, name, filmography)
        return redirect(url_for("views.profile_actor", item_id=item_id))

    query = Actor.query.filter_by(name_id=item_id).first_or_404()
    formatted_filmography = ", ".join([movie.title for movie in query.filmography])
    return render_template("name/edit.html", profile=query, filmography=formatted_filmography)


@bp.route("/name/<item_id>/delete")
@login_required
def delete_actor(item_id):
    util.remove_from_actor_table(item_id)
    return redirect(url_for("views.index"))
