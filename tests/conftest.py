from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from passportpal.api.main import create_app
from passportpal.config import Settings


@pytest.fixture
def client() -> Iterator[TestClient]:
    settings = Settings(app_env="ci")
    app = create_app(settings=settings)

    with TestClient(app) as test_client:
        yield test_client
