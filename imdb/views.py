from flask import Blueprint, render_template, request, redirect, url_for
from . import util
from sys import stderr
import json
import ast
bp = Blueprint("views", __name__)


@bp.route("/")
def index():
    return render_template("home/index.html", data=util.read_db())


@bp.route("/title/<item_id>")
def profile_tv(item_id):
    db = util.read_db()
    for p in db["tvShows"]:
        if p["id"] == item_id:
            return render_template("title/profile.html", profile=p)
    print(json.dumps(db, indent=4), stderr)
    return render_template("home/error.html")


@bp.route("/title/create", methods=["POST", "GET"])
def create_tv():
    db = util.read_db()
    item_id = len(db["tvShows"]) + len(db["actors"]) + 1
    if request.method == "POST":
        title = request.form["title"]
        cast = ast.literal_eval(request.form["cast"])
        util.save_to_db("tvShows", item_id, title, cast)
        return redirect(url_for("views.profile_tv", item_id=item_id))

    return render_template("/title/create.html")


@bp.route("/title/<item_id>/edit", methods=["POST", "GET"])
def edit_tv(item_id):
    db = util.read_db()

    if request.method == "POST":
        title = request.form["title"]
        cast = ast.literal_eval(request.form["cast"])
        util.save_to_db("tvShows", item_id, title, cast)
        return redirect(url_for("views.profile_tv", item_id=item_id))

    for p in db["tvShows"]:
        if p["id"] == item_id:
            return render_template("title/edit.html", profile=p)
    return render_template("home/error.html")


@bp.route("/title/<item_id>/delete", methods=["POST", "GET"])
def delete_tv(item_id):
    status = util.remove_from_db("tvShows", item_id)
    if status is False:
        return render_template("home/error.html")
    return redirect(url_for("views.index"))


# @bp.route("/name/<item_id>")
# def profile_actor(item_id):
#     db = util.read_db()
#     for p in db["actors"]:
#         if p["id"] == item_id:
#             return render_template("name/profile.html", profile=p)
#     return render_template("home/error.html")


# @bp.route("/name/create")
# def create_actor():
#     return render_template("name/create.html")


# @bp.route("/name/<item_id>/edit")
# def edit_actor(item_id):
#     db = util.read_db()
#     for p in db["actors"]:
#         if p["id"] == item_id:
#             return render_template("name/edit.html", profile=p)
#     return render_template("home/error.html")


# @bp.route("/name/<item_id>/save")
# def save_actor(item_id):
#     return


# @bp.route("/name/<item_id>/delete")
# def delete_actor(item_id):
#     return
