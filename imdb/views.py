from flask import Blueprint, render_template, request, redirect, url_for
from . import util
from .model import *
bp = Blueprint("views", __name__)


@bp.route("/")
def index():
    tv_shows = TvShow.query.order_by(TvShow.title).all()
    actors = Actor.query.order_by(Actor.name).all()
    return render_template("home/index.html", tv_shows=tv_shows, actors=actors)


###########
# TV SHOW #
###########
@bp.route("/title/<item_id>")
def profile_tv_show(item_id):
    query = TvShow.query.filter_by(title_id=item_id).first_or_404()
    return render_template("title/profile.html", profile=query)


@bp.route("/title/create", methods=["POST", "GET"])
def create_tv_show():
    if request.method == "POST":
        title = request.form["title"]
        cast = request.form["cast"].split(", ")
        item_id = util.add_to_tv_show_table(title, cast)
        return redirect(url_for("views.profile_tv_show", item_id=item_id))

    return render_template("/title/create.html")


@bp.route("/title/<item_id>/edit", methods=["POST", "GET"])
def edit_tv_show(item_id):
    if request.method == "POST":
        title = request.form["title"]
        cast = request.form["cast"].split(", ")
        util.save_to_tv_show_table(item_id, title, cast)
        return redirect(url_for("views.profile_tv_show", item_id=item_id))

    query = TvShow.query.filter_by(title_id=item_id).first_or_404()
    formatted_cast = ", ".join([actor.name for actor in query.cast])
    return render_template("title/edit.html", profile=query, cast=formatted_cast)


@bp.route("/title/<item_id>/delete", methods=["POST", "GET"])
def delete_tv_show(item_id):
    util.remove_from_tv_show_table(item_id)
    return redirect(url_for("views.index"))


#########
# ACTOR #
#########
@bp.route("/name/<item_id>")
def profile_actor(item_id):
    query = Actor.query.filter_by(name_id=item_id).first_or_404()
    return render_template("name/profile.html", profile=query)


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
    formatted_filmography = ", ".join([tv_show.title for tv_show in query.filmography])
    return render_template("name/edit.html", profile=query, filmography=formatted_filmography)


@bp.route("/name/<item_id>/delete", methods=["POST", "GET"])
def delete_actor(item_id):
    util.remove_from_actor_table(item_id)
    return redirect(url_for("views.index"))
