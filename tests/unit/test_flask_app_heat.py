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


def test_add_temps_200(tester):
    post_data = {
      "head_rest": 18,
      "back_rest": 21,
      "arm_rest": 23,
      "bum_rest": 22
    }
    response = tester.post("/heat/", json=post_data, follow_redirects=True)
    assert response.status_code == 200
    assert json.loads(response.data) == {"message": "ok"}


def test_add_temps_400_missing_body(tester):
    response = tester.post("/heat/", json={}, follow_redirects=True)
    assert response.status_code == 400
    assert json.loads(response.data) == {"message": "Lipseste body"}


def test_add_temps_400_missing_body_head_rest(tester):
    post_data = {
        "back_rest": 21,
        "arm_rest": 23,
        "bum_rest": 22
    }
    response = tester.post("/heat/", json=post_data, follow_redirects=True)
    assert response.status_code == 400
    assert json.loads(response.data) == {"message": "Valoare pt head_rest lipseste"}


def test_add_temps_400_missing_body_back_rest(tester):
    post_data = {
        "head_rest": 18,
        "arm_rest": 23,
        "bum_rest": 22
    }
    response = tester.post("/heat/", json=post_data, follow_redirects=True)
    assert response.status_code == 400
    assert json.loads(response.data) == {"message": "Valoare pt back_rest lipseste"}


def test_add_temps_400_missing_body_arm_rest(tester):
    post_data = {
        "head_rest": 18,
        "back_rest": 21,
        "bum_rest": 22
    }
    response = tester.post("/heat/", json=post_data, follow_redirects=True)
    assert response.status_code == 400
    assert json.loads(response.data) == {"message": "Valoare pt arm_rest lipseste"}


def test_add_temps_400_missing_body_bum_rest(tester):
    post_data = {
        "head_rest": 18,
        "back_rest": 21,
        "arm_rest": 23,
    }
    response = tester.post("/heat/", json=post_data, follow_redirects=True)
    assert response.status_code == 400
    assert json.loads(response.data) == {"message": "Valoare pt bum_rest lipseste"}


def test_add_temps_400_wrong_body_head_rest(tester):
    post_data = {
        "head_rest": "string",
        "back_rest": 21,
        "arm_rest": 23,
        "bum_rest": 22
    }
    response = tester.post("/heat/", json=post_data, follow_redirects=True)
    assert response.status_code == 400
    assert json.loads(response.data) == {"message": "Valoarea pt head_rest trebuie sa fie integer"}


def test_add_temps_400_wrong_body_back_rest(tester):
    post_data = {
        "head_rest": 18,
        "back_rest": "string",
        "arm_rest": 23,
        "bum_rest": 22
    }
    response = tester.post("/heat/", json=post_data, follow_redirects=True)
    assert response.status_code == 400
    assert json.loads(response.data) == {"message": "Valoarea pt back_rest trebuie sa fie integer"}


def test_add_temps_400_wrong_body_arm_rest(tester):
    post_data = {
        "head_rest": 18,
        "back_rest": 21,
        "arm_rest": "string",
        "bum_rest": 22
    }
    response = tester.post("/heat/", json=post_data, follow_redirects=True)
    assert response.status_code == 400
    assert json.loads(response.data) == {"message": "Valoarea pt arm_rest trebuie sa fie integer"}


def test_add_temps_400_wrong_body_bum_rest(tester):
    post_data = {
        "head_rest": 18,
        "back_rest": 21,
        "arm_rest": 23,
        "bum_rest": "string"
    }
    response = tester.post("/heat/", json=post_data, follow_redirects=True)
    assert response.status_code == 400
    assert json.loads(response.data) == {"message": "Valoarea pt bum_rest trebuie sa fie integer"}
