import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent.parent))


@pytest.fixture(scope="session")
def app():
    from app_flask import create_app

    app = create_app()
    yield app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()
