from .model import *


###########
# TV SHOW #
###########
def add_to_tv_show_table(item_title, item_cast):
    tv_show = TvShow(title=item_title)
    db.session.add(tv_show)
    for actor_name in item_cast:
        actor = Actor.query.filter_by(name=actor_name).first()
        if actor is None:
            actor = Actor(name=actor_name)
            db.session.add(actor)
        tv_show.cast.append(actor)
    db.session.commit()
    return tv_show.title_id


def save_to_tv_show_table(item_id, item_title, item_cast):
    tv_show = TvShow.query.filter_by(title_id=item_id).first()
    tv_show.title = item_title
    for actor_name in item_cast:
        actor = Actor.query.filter_by(name=actor_name).first()
        if actor is None:
            actor = Actor(name=actor_name)
            db.session.add(actor)
            tv_show.cast.append(actor)
        elif actor not in tv_show.cast:
            tv_show.cast.append(actor)
    for actor in tv_show.cast:
        if actor.name not in item_cast:
            tv_show.cast.remove(actor)
    db.session.commit()


def remove_from_tv_show_table(item_id):
    tv_show = TvShow.query.filter_by(title_id=item_id).first_or_404()
    db.session.delete(tv_show)
    db.session.commit()


#########
# ACTOR #
#########
def add_to_actor_table(item_name, item_filmography):
    actor = Actor(name=item_name)
    db.session.add(actor)
    for tv_show_title in item_filmography:
        tv_show = TvShow.query.filter_by(title=tv_show_title).first()
        if tv_show is None:
            tv_show = TvShow(title=tv_show_title)
            db.session.add(tv_show)
        actor.filmography.append(tv_show)
    db.session.commit()
    return actor.name_id


def save_to_actor_table(item_id, item_name, item_filmography):
    actor = Actor.query.filter_by(name_id=item_id).first()
    actor.name = item_name
    for tv_show_title in item_filmography:
        tv_show = TvShow.query.filter_by(title=tv_show_title).first()
        if tv_show is None:
            tv_show = TvShow(title=tv_show_title)
            db.session.add(tv_show)
            actor.filmography.append(tv_show)
        elif tv_show not in actor.filmography:
            actor.filmography.append(tv_show)
    for tv_show in actor.filmography:
        if tv_show.title not in item_filmography:
            actor.filmography.remove(tv_show)
    db.session.commit()


def remove_from_actor_table(item_id):
    actor = Actor.query.filter_by(name_id=item_id).first_or_404()
    db.session.delete(actor)
    db.session.commit()
