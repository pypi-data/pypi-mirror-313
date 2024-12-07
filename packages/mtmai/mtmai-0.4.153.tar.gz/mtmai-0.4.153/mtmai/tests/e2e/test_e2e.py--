import pytest
from fastapi.testclient import TestClient

from mtmai.server import build_app


@pytest.fixture(scope="module")
def test_app():
    app = build_app()
    client = TestClient(app)
    return client
