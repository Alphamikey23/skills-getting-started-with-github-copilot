import copy
import urllib.parse

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities before and after each test to avoid side effects."""
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))


def quote_path(s: str) -> str:
    # Helper for building safe URLs for activities with spaces
    return urllib.parse.quote(s, safe="")
