"""
Spotify service module.  It just does two things:

1) Get a token from Spotify using client credentials
2) Search for tracks and return some basic info
Author: Raquel Velis

--------------------------
| How to use the service |
--------------------------
# STEP 1: Get authentication token from Spotify
authentication_token = get_spotify_token()

# STEP 2: Search for a song using the token
results = search_songs_on_spotify("Hey Jude", "The Beatles", authentication_token)

# STEP 3: Display the first result
if results:
  first_song = results[0]
  print(f"Found: {first_song['name']} by {first_song['artists'][0]}")
"""

import os
import requests

# Endpoints
_SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
_SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"


def get_spotify_token():
    """Get a Spotify access token using client id/secret from environment variables."""
      """ Retrieve a Spotify access token using client credentials from environment variables.
    Returns:
        str: A valid Spotify access token.
    Raises:
        ValueError: If client ID or secret is missing.
        RuntimeError: If the token request fails or token is missing in the response.
    """
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError("Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET")

    # Make a simple POST request to get the token
    resp = requests.post(
        _SPOTIFY_TOKEN_URL,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )

    if resp.status_code != 200:
        raise RuntimeError("Could not get Spotify token")

    data = resp.json()
    token = data.get("access_token")
    # In most cases token_type is "Bearer". We'll just return the token.
    if not token:
        raise RuntimeError("Token not found in response")
    return token

def search_songs_on_spotify(title, artist, token, limit=5):
    """Search for tracks on Spotify and return a simple list of dictionaries."""
    if not token:
        raise ValueError("Token is required")

    # Build the query like: track:TITLE [artist:ARTIST]
    q = f"track:{str(title).strip()}"
    if artist:
        q += f" artist:{str(artist).strip()}"

    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": q,
        "type": "track",
        "limit": str(limit),
    }
# Send request to Spotify search endpoint
    resp = requests.get(_SPOTIFY_SEARCH_URL, headers=headers, params=params)

    if resp.status_code != 200:
        raise RuntimeError("Spotify search failed")

    payload = resp.json()
    items = (
        (payload or {}).get("tracks") or {}
    ).get("items") or []

    results = []
    for item in items:
        # Be very defensive and use .get everywhere
        album = item.get("album") or {}
        artists_list = item.get("artists") or []
        external_urls = item.get("external_urls") or {}
        simple_artists = []
        for a in artists_list:
            name = None
            if isinstance(a, dict):
                name = a.get("name")
            if name:
                simple_artists.append(name)

        result = {
            "id": item.get("id"),
            "name": item.get("name"),
            "artists": simple_artists,
            "album": album.get("name"),
            "release_date": album.get("release_date"),
            "duration_ms": item.get("duration_ms"),
            "popularity": item.get("popularity"),
            "preview_url": item.get("preview_url"),
            "external_url": external_urls.get("spotify"),
            "images": album.get("images") or [],
        }
        results.append(result)

    return results


__all__ = ["get_spotify_token", "search_songs_on_spotify"]
