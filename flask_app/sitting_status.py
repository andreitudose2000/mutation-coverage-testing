from flask_app.db import get_db
from flask_app import utils

flask_app = None

def set_sitting_status(is_sitting):
    if not (isinstance(is_sitting, bool) or (isinstance(is_sitting, int) and is_sitting in [0, 1])):
        raise ValueError

    db = get_db()
    db.execute("INSERT INTO user_sitting (is_sitting) VALUES (?)",
               (int(is_sitting),))
    db.commit()
    print(f"## Updated in db table 'user_sitting' - 'is_sitting' = {is_sitting}")
    return True


def get_sitting_status():
    db = get_db()
    status = db.execute(
        'SELECT id, is_sitting, updated_on \
        FROM user_sitting \
        ORDER BY updated_on DESC'
    ).fetchone()
    return utils.dict_from_row(status) if status is not None else None
