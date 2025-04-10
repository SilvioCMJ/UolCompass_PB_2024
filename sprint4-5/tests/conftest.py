import pytest
from typing import Any, Generator
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, Any, None]:
    with TestClient(app, "http://test") as client:
        yield client
