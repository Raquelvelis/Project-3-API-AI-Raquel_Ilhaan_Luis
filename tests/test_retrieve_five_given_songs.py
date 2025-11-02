import types
import os
import sys
from typing import Dict, Any, List, Tuple

import pytest

# Ensure project root is on sys.path for direct module import when tests run from a different CWD
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import spotify_service as ss


class _StubResponse:
    def __init__(self, status_code: int, payload: Dict[str, Any]):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        return self._payload


def _build_track_payload(track_name: str, artist_name: str) -> Dict[str, Any]:
    return {
        "tracks": {
            "items": [
                {
                    "id": f"mock-{track_name.lower().replace(' ', '-')}-{artist_name.lower().replace(' ', '-')}",
                    "name": track_name,
                    "artists": [{"name": artist_name}],
                    "album": {
                        "name": f"{track_name} (Single)",
                        "release_date": "2011-01-01",
                        "images": [],
                    },
                    "duration_ms": 180000,
                    "popularity": 80,
                    "preview_url": None,
                    "external_urls": {"spotify": "https://open.spotify.com/track/mock"},
                }
            ]
        }
    }


def test_retrieve_five_given_songs(mocker):
    # Prepare five known (title, artist) pairs
    songs: List[Tuple[str, str]] = [
        ("Hey Jude", "The Beatles"),
        ("Shape of You", "Ed Sheeran"),
        ("Billie Jean", "Michael Jackson"),
        ("Rolling in the Deep", "Adele"),
        ("Smells Like Teen Spirit", "Nirvana"),
    ]

    # Mock token request to return a static bearer token
    def _mock_post(url, data=None, auth=None, timeout=None):
        assert url.endswith("/api/token")
        assert data == {"grant_type": "client_credentials"}
        assert isinstance(auth, tuple) and len(auth) == 2
        payload = {"access_token": "mock-token", "token_type": "Bearer", "expires_in": 3600}
        return _StubResponse(200, payload)

    mocker.patch.object(ss.requests, "post", side_effect=_mock_post)

    # Mock search endpoint. It will inspect the query to craft a matching payload
    def _mock_get(url, headers=None, params=None, timeout=None):
        assert url.endswith("/v1/search")
        assert headers and headers.get("Authorization") == "Bearer mock-token"
        assert params and params.get("type") == "track"
        q = params.get("q") or ""
        # q is of the form "track:TITLE" or "track:TITLE artist:ARTIST"; titles/artists may contain spaces
        track_name = "Unknown"
        artist_name = "Unknown Artist"
        if q.startswith("track:"):
            if " artist:" in q:
                track_part, artist_part = q.split(" artist:", 1)
                track_name = track_part[len("track:"):].strip()
                artist_name = artist_part.strip()
            else:
                track_name = q[len("track:"):].strip()
        return _StubResponse(200, _build_track_payload(track_name, artist_name))

    mocker.patch.object(ss.requests, "get", side_effect=_mock_get)

    # Set dummy environment credentials expected by get_spotify_token
    mocker.patch.dict(os.environ, {
        "SPOTIFY_CLIENT_ID": "dummy-client",
        "SPOTIFY_CLIENT_SECRET": "dummy-secret",
    }, clear=False)

    # Acquire token (uses mocked POST)
    token = ss.get_spotify_token()
    assert token == "mock-token"

    # For each given song, search and validate at least one normalized result
    for title, artist in songs:
        results = ss.search_songs_on_spotify(title, artist, token, limit=5)
        assert isinstance(results, list)
        assert len(results) >= 1
        top = results[0]
        # basic shape validation
        for key in ["id", "name", "artists", "album", "release_date", "duration_ms", "popularity", "preview_url", "external_url", "images"]:
            assert key in top
        # correctness checks from our mocked payload
        assert top["name"] == title
        assert artist in top["artists"]
        assert isinstance(top["images"], list)
