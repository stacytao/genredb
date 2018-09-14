import json

db_file = "db.json"

profile_types = {
    "tvShows": {
        "identifier": "title",
        "collection": "cast"
    },
    "actors": {
        "identifier": "name",
        "collection": "filmography"
    }
}


def save_to_db(profile_type, item_id, identifier, collection):
    db = read_db()
    if int(item_id) > (len(db["tvShows"]) + len(db["actors"])):
        db[profile_type].append({
            "id": item_id,
            get_identifier(profile_type): identifier,
            get_collection(profile_type): collection
        })
    else:
        for p in db[profile_type]:
            if p["id"] == item_id:
                p[get_identifier(profile_type)] = identifier
                p[get_collection(profile_type)] = collection
                break
    write_db(db)


def remove_from_db(profile_type, item_id):
    db = read_db()
    for p in db[profile_type]:
        if p["id"] == item_id:
            db[profile_type].remove(p)
            write_db(db)
            return True
    return False


def read_db():
    with open(db_file) as json_file:
        db = json.load(json_file)
        return db


def write_db(db):
    with open(db_file, "w") as outfile:
        json.dump(db, outfile, indent=4)


def get_identifier(profile_type):
    return profile_types[profile_type]["identifier"]


def get_collection(profile_type):
    return profile_types[profile_type]["collection"]
