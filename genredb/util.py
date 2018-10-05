import json
from .model import *


def init_db():
    db.create_all()
    with open('/Users/Stacy/Documents/Columbia/Junior Year/IMDb/genredb/movies_2000.json') as f:
        data = json.load(f)
        for movie in data:
            try:
                title = movie["title"]
                year = movie["year"]
                cast = clean_cast(movie["cast"].split(", "))
                genres = clean_genres(movie["genre"].split(", "))

                add_to_movie_table(title, year, cast, genres)
            except:
                print("Did not add {}".format(movie["title"]))


def clean_cast(cast):
    while "Jr." in cast:
        cast[cast.index("Jr.") - 1] += ", Jr."
        cast.pop(cast.index("Jr."))
    return set(cast)


def clean_genres(genres):
    invalid_genres = set([
        "007",
        "3D",
        "Biblical",
        "Boxing",
        "Buddy cop",
        "Christian",
        "Direct-to-DVD",
        "Independent movie",
        "Neo-noir",
        "Reality",
        "Road",
        "Social",
        "Survival",
        "reality",
        "swashbuckler"]
    )
    genre_replacements = {
        "Action Adventure Science fiction": ["Action", "Adventure", "Science Fiction"],
        "Action Thriller": ["Action", "Thriller"],
        "Action adventure": ["Action", "Adventure"],
        "Action comedy": ["Action", "Comedy"],
        "Action drama": ["Action", "Drama"],
        "Action film": ["Action"],
        "Action horror": ["Action", "Horror"],
        "Action thriller": ["Action", "Thriller"],
        "Action-adventure": ["Action", "Adventure"],
        "Action-comedy": ["Action", "Comedy"],
        "Action-thriller": ["Action", "Thriller"],
        "Adventure Science fiction": ["Adventure", "Science Fiction"],
        "Adventure drama": ["Adventure", "Drama"],
        "Adventure-Comedy": ["Adventure", "Comedy"],
        "Adventure/Comedy/Drama/Family": ["Adventure", "Comedy", "Drama", "Family"],
        "Animated film": ["Animated"],
        "Animation": ["Animated"],
        "Bio-pic": ["Biography"],
        "Biographical": ["Biography"],
        "Biopic": ["Biography"],
        "Black comedy": ["Comedy"],
        "Buddy comedy": ["Comedy"],
        "Christian drama": ["Drama"],
        "Comedy Fantasy film": ["Comedy", "Fantasy"],
        "Comedy drama": ["Comedy", "Drama"],
        "Comedy horror": ["Comedy", "Horror"],
        "Comedy-drama": ["Comedy", "Drama"],
        "Comedy/Drama": ["Comedy", "Drama"],
        "Comedy/Drama/Romance": ["Comedy", "Drama", "Romance"],
        "Coming of age": ["Teen"],
        "Crime comedy": ["Crime", "Comedy"],
        "Crime drama": ["Crime", "Drama"],
        "Crime thriller": ["Crime", "Thriller"],
        "Crime/Drama/Mystery/Romance/Thriller": ["Crime", "Drama", "Mystery", "Romance", "Thriller"],
        "Dark comedy": ["Comedy"],
        "Disaster film": ["Disaster"],
        "Docudrama": ["Documentary", "Drama"],
        "Drama Horror Thriller Film": ["Drama", "Horror", "Thriller"],
        "Drama comedy": ["Drama", "Comedy"],
        "Dramatic comedy": ["Drama", "Comedy"],
        "Dramedy": ["Drama", "Comedy"],
        "Drana": ["Drama"],
        "Epic Fantasy,": ["Epic", "Fantasy"],
        "Epic,": ["Epic"],
        "Erotic thriller": ["Erotic", "Thriller"],
        "Family film": ["Family"],
        "Fantasy Thriller": ["Fantasy", "Thriller"],
        "Fantasy romance": ["Fantasy", "Romance"],
        "Fantasy-comedy": ["Fantasy", "Comedy"],
        "Found footage": ["Found Footage"],
        "Historical Drama": ["Historical"],
        "Historical drama": ["Historical"],
        "Horror comedy": ["Horror", "Comedy"],
        "Horror film": ["Horror"],
        "Horror thriller": ["Horror", "Thriller"],
        "Horror-thriller": ["Horror", "Thriller"],
        "Horror–Thriller": ["Horror", "Thriller"],
        "LGBT-themed comedy-drama": ["Drama", "Comedy"],
        "Legal drama": ["Legal", "Drama"],
        "Live action": ["Live Action"],
        "Live-action": ["Live Action"],
        "Live-action/animated film": ["Live Action", "Animated"],
        "Martial arts": ["Martial Arts"],
        "Martial arts/Horror/Comedy": ["Martial Arts", "Horror", "Comedy"],
        "Mockumentary": ["Mockumentary", "Satire"],
        "Music": ["Musical"],
        "Musical comedy": ["Musical", "Comedy"],
        "Musical drama": ["Musical", "Drama"],
        "Mystery-Drama": ["Mystery", "Drama"],
        "Nature documentary": ["Documentary"],
        "Parody": ["Satire"],
        "Performance film": ["Performance"],
        "Political Thriller": ["Political", "Thriller"],
        "Political documentary": ["Political", "Documentary"],
        "Political drama": ["Political", "Drama"],
        "Political thriller": ["Political", "Thriller"],
        "Psychological Horror": ["Horror"],
        "Psychological horror": ["Horror"],
        "Psychological thriller": ["Thriller"],
        "Rockumentary": ["Musical", "Documentary"],
        "Rom com": ["Romance", "Comedy"],
        "Romance-horror": ["Romance", "Horror"],
        "Romantic": ["Romance"],
        "Romantic Comedy": ["Romance", "Comedy"],
        "Romantic Drama": ["Romance", "Drama"],
        "Romantic comedy": ["Romance", "Comedy"],
        "Romantic comedy-Drama": ["Romance", "Comedy", "Drama"],
        "Romantic drama": ["Romance", "Drama"],
        "Romantic fantasy": ["Romance", "Fantasy"],
        "Romantic thriller": ["Romance", "Thriller"],
        "Romantic-comedy": ["Romance", "Comedy"],
        "Sci-Fi": ["Science Fiction"],
        "Sci-fi": ["Science Fiction"],
        "Sci-fi comedy": ["Science Fiction", "Comedy"],
        "Sci-fi drama": ["Science Fiction", "Drama"],
        "Sci-fi horror": ["Science Fiction", "Horror"],
        "Sci-fi western": ["Science Fiction", "Western"],
        "Science fiction": ["Science Fiction"],
        "Science fiction Mystery": ["Science Fiction", "Mystery"],
        "Science fiction Thriller": ["Science Fiction", "Thriller"],
        "Science-fiction": ["Science Fiction"],
        "Slahser": ["Slasher"],
        "Slasher": ["Slasher"],
        "Solution-mentary": ["Documentary"],
        "Spoof": ["Satire"],
        "Sports comedy": ["Sports", "Comedy"],
        "Spy film": ["Spy"],
        "Spy thriller": ["Spy", "Thriller"],
        "Supernatural horror": ["Supernatural", "Horror"],
        "Supernatural thriller": ["Supernatural", "Thriller"],
        "Suspense": ["Suspense"],
        "Suspense thriller": ["Thriller"],
        "Teen": ["Teen"],
        "War drama": ["War", "Drama"],
        "War film": ["War"],
        "War/Horror": ["War", "Horror"],
        "Western drama": ["Western", "Drama"],
        "comedy": ["Comedy"],
        "crime": ["Crime"],
        "dance": ["Dance"],
        "drama": ["Drama"],
        "family": ["Family"],
        "fantasy": ["Fantasy"],
        "history": ["Historical"],
        "horror": ["Horro"],
        "live-action/animation": ["Live Action", "Animated"],
        "musical": ["Musical"],
        "parody": ["Satire"],
        "romance": ["Romance"],
        "romantic comedy": ["Romance", "Comedy"],
        "sci-fi": ["Science Fiction"],
        "silent": ["Silent"],
        "sports": ["Sports"],
        "spy": ["Spy"],
        "superhero": ["Superhero"],
        "teen": ["Teen"],
        "thriller": ["Thriller"],
        "war": ["War"],
        "western": ["Western"]
    }
    cleaned_genres = set([])

    for g in genres:
        if g in genre_replacements:
            for replacement in genre_replacements[g]:
                cleaned_genres.add(replacement)
        elif g not in invalid_genres:
            cleaned_genres.add(g)
    return cleaned_genres


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
