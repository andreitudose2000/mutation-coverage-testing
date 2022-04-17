import os
import json
import tempfile
from datetime import datetime, timedelta

import pytest

from flask_app import create_app, utils


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

@pytest.mark.skip
def add_one_row_to_db(tester):
    post_data = {
        "user_height": 180
    }
    response = tester.post("/userInfo/", json=post_data, follow_redirects=True)
    return response, post_data


def test_post_heat_check_heat_200(tester):
    post_data = {
        "head_rest": 18,
        "back_rest": 21,
        "arm_rest": 23,
        "bum_rest": 22
    }
    response = tester.post("/heat", json=post_data, follow_redirects=True)
    assert response.status_code == 200
    assert json.loads(response.data) == {"message": "ok"}
    response1 = tester.get("/userInfo", follow_redirects=True)
    assert response1.status_code == 404
    data = json.loads(response1.data)
    print(data)



def test_post_heat_get_userInfo_redirect(tester):
    post_data = {
        "head_rest": 18,
        "back_rest": 21,
        "arm_rest": 23,
        "bum_rest": 22
    }
    response = tester.post("/heat", json=post_data)
    assert response.status_code == 308
    # assert json.loads(response.data) == {"message": "ok"}
    response = tester.get("/userInfo", follow_redirects=True)
    assert response.status_code == 404


def test_user_info_heat_get_200(tester):
    post_data = {
        "head_rest": 18,
        "back_rest": 21,
        "arm_rest": 23,
        "bum_rest": "twenty two"
    }
    response = tester.post("/heat", json=post_data, follow_redirects=True)
    assert response.status_code == 400
    assert json.loads(response.data) == {"message": "Valoarea pt bum_rest trebuie sa fie integer"}
    _, post_data = add_one_row_to_db(tester)
    response1 = tester.get("/userInfo", follow_redirects=True)
    assert response1.status_code == 200
    data = json.loads(response1.data)
    print(data)
    assert data["id"] == 1 \
           and data["user_height"] == post_data["user_height"] \
           and data["chair_height"] == utils.chair_height_formula(post_data["user_height"]) \
           and data["desk_height"] == utils.desk_height_formula(post_data["user_height"])


def test_post_heat_post_weight_redirect(tester):
    post_data = {
        "head_rest": 18,
        "back_rest": 21,
        "arm_rest": 23,
        "bum_rest": 22
    }
    response = tester.post("/heat", json=post_data)
    assert response.status_code == 308

    from flask_app.weight import add_weight_to_db

    add_weight_to_db(80)
    add_weight_to_db(90)
    add_weight_to_db(100)
    now = datetime.now()
    response1 = tester.get("/weight/history", follow_redirects=True)
    assert response1.status_code == 200
    data = json.loads(response1.data)
    assert isinstance(data, list)
    assert len(data) == 3
    assert any(x["id"] == 1 and x["mass"] == 80
               and now - datetime.strptime(x['updated_on'], '%Y-%m-%d %H:%M:%S') < timedelta(0, 5) for x in data)
    assert any(x["id"] == 2 and x["mass"] == 90
               and now - datetime.strptime(x['updated_on'], '%Y-%m-%d %H:%M:%S') < timedelta(0, 5) for x in data)
    assert any(x["id"] == 3 and x["mass"] == 100
               and now - datetime.strptime(x['updated_on'], '%Y-%m-%d %H:%M:%S') < timedelta(0, 5) for x in data)


def test_get_weight_post_heat_redirect(tester):
    response = tester.get("/weight/history")
    assert response.status_code == 200
    post_data = {
        "head_rest": 18,
        "back_rest": 21,
        "arm_rest": 23,
        "bum_rest": "twenty two"
    }
    response1 = tester.post("/heat", json=post_data, follow_redirects=True)
    assert response1.status_code == 400
    assert json.loads(response1.data) == {"message": "Valoarea pt bum_rest trebuie sa fie integer"}


def test_get_measure_get_history(tester):
    response = tester.get("/weight/measure")
    assert response.status_code == 200
    response1 = tester.get("/weight/history", follow_redirects=True)
    assert response1.status_code == 200


def test_set_sitting_status_post_heat_bad(tester):
    import flask_app.sitting_status as sitting_status_manager
    sitting_status_manager.set_sitting_status(True)
    now = datetime.now()
    status = sitting_status_manager.get_sitting_status()
    assert status["id"] == 1
    assert status["is_sitting"] == 1
    assert now - datetime.strptime(status["updated_on"], '%Y-%m-%d %H:%M:%S') < timedelta(0, 5)
    post_data = {
        "head_rest": 18,
        "back_rest": 21,
        "arm_rest": 23,
        "bum_rest": "integration test"
    }
    response1 = tester.post("/heat", json=post_data, follow_redirects=True)
    assert response1.status_code == 400
    assert json.loads(response1.data) == {"message": "Valoarea pt bum_rest trebuie sa fie integer"}


def test_set_sitting_status_post_heat_ok(tester):
    import flask_app.sitting_status as sitting_status_manager
    sitting_status_manager.set_sitting_status(True)
    now = datetime.now()
    status = sitting_status_manager.get_sitting_status()
    assert status["id"] == 1
    assert status["is_sitting"] == 1
    assert now - datetime.strptime(status["updated_on"], '%Y-%m-%d %H:%M:%S') < timedelta(0, 5)
    post_data = {
        "head_rest": 18,
        "back_rest": 21,
        "arm_rest": 23,
        "bum_rest": 22
    }
    response1 = tester.post("/heat", json=post_data, follow_redirects=True)
    assert response1.status_code == 200
    assert json.loads(response1.data) == {"message": "ok"}

def test_get_weight_set_sitting_status_bad(tester):
    import flask_app.sitting_status as sitting_status_manager
    sitting_status_manager.set_sitting_status(True)
    now = datetime.now()
    status = sitting_status_manager.get_sitting_status()
    assert status["id"] == 1
    assert status["is_sitting"] == 1
    assert now - datetime.strptime(status["updated_on"], '%Y-%m-%d %H:%M:%S') < timedelta(0, 5)
    response = tester.get("/weight/istorie")
    assert response.status_code == 404
