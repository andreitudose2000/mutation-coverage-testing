import json
import os
import tempfile
from datetime import datetime, timedelta

import pytest

from flask_app import create_app


@pytest.fixture()
def tester():
    # creez un fisier nou temporar .sqlite unde va fi stocata baza de date
    db_fd, dbfile = tempfile.mkstemp(suffix=".sqlite")
    app = create_app("flask_configurations.TestingConfig", db_file=dbfile)

    # returnez clientul tester cu setarea de mai sus
    with app.test_client() as tester:
        with app.app_context():
            yield tester

    # inchid file descriptorul
    os.close(db_fd)
    # sterg fisierul de pe disk
    os.unlink(app.config['DATABASE'])


def test_measure_get(tester):
    response = tester.get("/weight/measure")
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data)
    assert "weight" in data
    assert 70 <= int(data["weight"]) <= 100


def test_history_get(tester):
    response = tester.get("/weight/history", follow_redirects=True)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 0


def test_history_get_with_data(tester):
    from flask_app.weight import add_weight_to_db
    add_weight_to_db(80)
    add_weight_to_db(90)
    add_weight_to_db(100)
    now = datetime.now()
    response = tester.get("/weight/history", follow_redirects=True)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 3
    assert any(x["id"] == 1 and x["mass"] == 80
               and now - datetime.strptime(x['updated_on'], '%Y-%m-%d %H:%M:%S') < timedelta(0, 5) for x in data)
    assert any(x["id"] == 2 and x["mass"] == 90
               and now - datetime.strptime(x['updated_on'], '%Y-%m-%d %H:%M:%S') < timedelta(0, 5) for x in data)
    assert any(x["id"] == 3 and x["mass"] == 100
               and now - datetime.strptime(x['updated_on'], '%Y-%m-%d %H:%M:%S') < timedelta(0, 5) for x in data)


def test_add_weight_to_db_error(tester):
    from flask_app.weight import add_weight_to_db
    with pytest.raises(ValueError):
        add_weight_to_db(None)
    with pytest.raises(ValueError):
        add_weight_to_db("string")
    with pytest.raises(ValueError):
        add_weight_to_db(2+3j)
