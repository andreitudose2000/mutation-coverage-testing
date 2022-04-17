from flask import (Blueprint, request, jsonify)
from flask_app.db import get_db
from flask_app import utils

bp = Blueprint('userInfo', __name__, url_prefix='/userInfo')

@bp.route('/', methods=(['GET']))
def getUserInfoEndpoint():
    userInfo = getUserInfo()

    if userInfo is None:
        return jsonify(message="Nu exista setari pentru utilizator"), 404

    return jsonify({
        "id": userInfo["id"],
        "user_height": userInfo["user_height"],
        "chair_height": userInfo["chair_height"],
        "desk_height": userInfo["desk_height"],
        "updated_on": userInfo["updated_on"]
    }), 200

def getUserInfo():
    userInfo = get_db().execute(
        'SELECT id, user_height, chair_height, desk_height, updated_on \
        FROM user_info \
        ORDER BY updated_on DESC'
    ).fetchone()

    return userInfo

@bp.route('/', methods=(['POST']))
def setUserInfoEndpoint():
    if not request.json:
        return jsonify(message="Nu ati trimis setari"), 400
    if 'user_height' not in request.json:
        return jsonify(message="Nu ati trimis 'user_height'"), 400

    user_height: int

    try:
        user_height = int(request.json["user_height"])
        if user_height < 100 or user_height > 250:
            return jsonify(message='Valoare exagerata pentru "user_height"'), 400
    except ValueError:
        return jsonify(message='"user_height" trebuie sa fie integer'), 400

    db = get_db()
    chair_height = utils.chair_height_formula(user_height)
    desk_height = utils.desk_height_formula(user_height)
    try:
        db.execute("INSERT INTO user_info (user_height, chair_height, desk_height) VALUES (?, ?, ?)",
                   (user_height, chair_height, desk_height))
        db.commit()
        print(f"## Updated in db table 'user_info' - 'user_height' = {user_height}; 'chair_height'={chair_height}; "
              f"'desk_height'={desk_height}")
    except db.Error:
        return jsonify(message="Eroare la introducerea in baza de date"), 400

    return jsonify(message="Setari actualizate cu succes"), 201

