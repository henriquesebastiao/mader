import pytest
from fastapi.testclient import TestClient

from mader.app import app


@pytest.fixture
def client():
    return TestClient(app)
