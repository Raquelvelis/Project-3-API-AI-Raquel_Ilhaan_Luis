import os
import sys
from typing import List, Dict, Any

import pytest

# Optionally load environment variables from a local .env file if present
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    # If python-dotenv isn't available at runtime, proceed without it
    pass

# Ensure the project's root is on sys.path for direct module import when tests run from a different CWD
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if PROJECT_ROOT not in sys.path:
     sys.path.insert(0, PROJECT_ROOT)

import spotify_service as ss

@pytest.mark.integration
def test_search_songs_on_spotify_integration():
    """Integration test that calls the real Spotify Web API.

    This test is skipped automatically if SPOTIFY_CLIENT_ID/SECRET are not set.
    It performs live HTTP requests to obtain a token and search for a well-known track.
    """
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        pytest.skip("Skipping integration test: SPOTIFY_CLIENT_ID/SECRET not set")

    # Acquire a real token
    token = ss.get_spotify_token()
    assert isinstance(token, str) and token, "Expected a non-empty token string"

    # Search for a well-known song with artist
    title = "Hey Jude"
    artist = "The Beatles"
    results: List[Dict[str, Any]] = ss.search_songs_on_spotify(title, artist, token, limit=5)

    assert isinstance(results, list)
    assert len(results) >= 1, "Expected at least one result from Spotify search"

    # Validate basic shape for the first item
    top = results[0]
    for key in [
        "id",
        "name",
        "artists",
        "album",
        "release_date",
        "duration_ms",
        "popularity",
        "preview_url",
        "external_url",
        "images",
    ]:
        assert key in top

    # Validate that at least one of the returned items plausibly matches the query
    def _matches(item: Dict[str, Any]) -> bool:
        name_ok = isinstance(item.get("name"), str) and "hey jude" in item["name"].lower()
        artists = item.get("artists") or []
        artist_ok = any(isinstance(a, str) and "beatles" in a.lower() for a in artists)
        return name_ok and artist_ok

    assert any(_matches(item) for item in results), "No results matched expected title/artist"

    # Also verify that searching only by title returns results
    title_only_results = ss.search_songs_on_spotify(title, None, token, limit=3)
    assert isinstance(title_only_results, list)
    assert len(title_only_results) >= 1
