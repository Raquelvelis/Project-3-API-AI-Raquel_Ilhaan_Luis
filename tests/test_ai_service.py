import pytest
from gemini import get_songs

def test_get_songs_valid_mood(mocker):
    mock_response = type("MockResponse", (), {
        "text": "Imagine - John Lennon - Imagine"
    })()

    mocker.patch("google.generativeai.GenerativeModel.generate_content", return_value=mock_response)
    mocker.patch("gemini.get_spotify_token", return_value="mock-token")
    mocker.patch("gemini.search_songs_on_spotify", return_value=[{"external_url": "https://open.spotify.com/track/mock"}])

    songs = get_songs("happy")
    assert isinstance(songs, list)
    assert songs[0].title == "Imagine"
    assert songs[0].spotify_url.startswith("https://")

def test_get_songs_empty_mood(mocker):
    mock_response = type("MockResponse", (), {
        "text": ""
    })()
    mocker.patch("google.generativeai.GenerativeModel.generate_content", return_value=mock_response)
    songs = get_songs("")
    assert songs == []

def test_get_songs_invalid_api_key(mocker):
    mocker.patch("google.generativeai.GenerativeModel.generate_content", side_effect=Exception("Invalid API key"))
    songs = get_songs("sad")
    assert songs == []
