from datetime import datetime
from flask import (Blueprint, g, request, jsonify)
from flask_app.db import get_db
import random

bp = Blueprint('weight', __name__, url_prefix='/weight')

def measure_weight():
    return random.randint(70, 100)

def add_weight_to_db(weight):
    if not isinstance(weight, int) and not isinstance(weight, float):
        raise ValueError
    db = get_db()
    db.execute(
        "INSERT INTO user_weight (mass) VALUES (?)",
        (weight,),
    )
    db.commit()
    print(f"## Updated in db table 'user_weight' - 'weight' = {weight}")

def get_current_weight():
    weight = measure_weight()
    add_weight_to_db(weight)
    return weight

def get_historic_weight():
    db = get_db()
    entrys = db.execute(
        "SELECT * FROM user_weight", ()
    ).fetchall()
    res = []
    for x in entrys:
        res.append({'id' : x['id'], 'mass' : x['mass'], 'updated_on' : x['updated_on']})
    return res

@bp.route('/measure', methods=(['GET']))
def get_weight():
    weight = get_current_weight()
    return jsonify(weight = weight), 200

@bp.route('/history', methods=(['GET']))
def report_weight():
    res = get_historic_weight()
    return jsonify(res), 200
