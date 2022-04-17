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


def test_set_sitting_status(tester):
    import flask_app.sitting_status as sitting_status_manager
    sitting_status_manager.set_sitting_status(True)
    now = datetime.now()
    status = sitting_status_manager.get_sitting_status()
    assert status["id"] == 1
    assert status["is_sitting"] == 1
    assert now - datetime.strptime(status["updated_on"], '%Y-%m-%d %H:%M:%S') < timedelta(0, 5)


def test_set_sitting_status_error(tester):
    import flask_app.sitting_status as sitting_status_manager
    with pytest.raises(ValueError):
        sitting_status_manager.set_sitting_status(None)
    with pytest.raises(ValueError):
        sitting_status_manager.set_sitting_status(-1)
    with pytest.raises(ValueError):
        sitting_status_manager.set_sitting_status(2)
    sitting_status_manager.set_sitting_status(0)
    sitting_status_manager.set_sitting_status(1)
    sitting_status_manager.set_sitting_status(True)
    sitting_status_manager.set_sitting_status(False)
