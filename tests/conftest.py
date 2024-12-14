import os
import sys
from os import path

os.environ["APP_ENV"] = "TEST"

_root_path = path.realpath(path.join(path.dirname(__file__), "..", "src"))
sys.path.append(_root_path)

import pytest

from main import app
from starlette.testclient import TestClient


@pytest.fixture(scope="session")
def db():
    return app.container.db()


@pytest.fixture(scope="session")
def api(db):
    _client = TestClient(app)
    # _client = app.test_client()

    # db.drop_all()
    # db.create_all()

    return _client
