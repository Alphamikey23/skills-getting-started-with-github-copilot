import urllib.parse

from src import app as _app  # alias to avoid shadowing


def quote(value: str) -> str:
    return urllib.parse.quote(value, safe="")


# simple helper to use the TestClient fixture

def test_get_activities_returns_list(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity_success(client):
    email = "newstudent@example.com"
    activity = "Chess Club"

    # signup
    response = client.post(f"/activities/{quote(activity)}/signup?email={urllib.parse.quote(email)}")
    assert response.status_code == 200
    body = response.json()
    assert "Signed up" in body["message"]

    # ensure participant is now listed
    resp2 = client.get("/activities")
    assert email in resp2.json()[activity]["participants"]


def test_signup_duplicate_returns_400(client):
    email = "michael@mergington.edu"  # already a participant
    activity = "Chess Club"

    response = client.post(f"/activities/{quote(activity)}/signup?email={urllib.parse.quote(email)}")
    assert response.status_code == 400


def test_unregister_participant_success(client):
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # remove participant
    response = client.delete(f"/activities/{quote(activity)}/unregister?email={urllib.parse.quote(email)}")
    assert response.status_code == 200
    body = response.json()
    assert "Unregistered" in body["message"]

    # ensure participant removed
    resp2 = client.get("/activities")
    assert email not in resp2.json()[activity]["participants"]


def test_unregister_nonexistent_participant_returns_404(client):
    activity = "Chess Club"
    email = "not-here@example.com"

    response = client.delete(f"/activities/{quote(activity)}/unregister?email={urllib.parse.quote(email)}")
    assert response.status_code == 404


def test_unregister_nonexistent_activity_returns_404(client):
    activity = "NoSuchActivity"
    email = "someone@example.com"

    response = client.delete(f"/activities/{quote(activity)}/unregister?email={urllib.parse.quote(email)}")
    assert response.status_code == 404
