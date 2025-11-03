from types import SimpleNamespace
from app import app

def test_get_mood_valid(mocker):
    client = app.test_client()
    mock_songs = [
        SimpleNamespace(
            title="Imagine",
            artist="John Lennon",
            album="Imagine",
            spotify_url="https://open.spotify.com/track/mock"
        )
    ]
    # ✅ Patch where get_songs is used — in app.py
    mocker.patch("app.get_songs", return_value=mock_songs)

    response = client.get("/get_mood?Mood=happy")
    assert response.status_code == 200
    assert b"Imagine" in response.data

def test_get_mood_empty(mocker):
    client = app.test_client()
    mocker.patch("app.get_songs", return_value=[])
    response = client.get("/get_mood?Mood=")
    assert response.status_code == 200
    assert b"No spotify link found" in response.data
