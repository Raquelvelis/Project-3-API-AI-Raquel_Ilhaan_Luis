# Author: Raquel Velis
# Description: Uses Gemini API to generate mood-based song recommendations and enriches them with Spotify links.
from google import genai
from google.genai import types
from pydantic import BaseModel
import os
from spotify_service import get_spotify_token, search_songs_on_spotify

class Song(BaseModel): # creates a structure for geminis JSON response
    """ Represents a song recommendation returned by Gemini.
    Attributes:
        title (str): Title of the song.
        artist (str): Artist name.
        album (str): Album name.
        spotify_url (str): Link to the song on Spotify.
    """
    title: str
    artist: str
    album: str
    spotify_url: str

# Load Gemini API key from environment
GOOGLE_API_KEY = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=GOOGLE_API_KEY)

def get_songs(mood: str):
    """Generate a list of song recommendations based on the user's mood using Gemini,
    and enrich each song with a Spotify link.
    Args:
        mood (str): The user's mood or genre input.
    Returns:
        list[Song]: A list of Song objects with Gemini metadata and Spotify URLs.
    """
    # Generate song recommendations using Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        You are Moodify. Recommend 5 songs based on the user's mood.
        If the user specifies a genre, recommend 5 songs in that genre.
        If not, choose a random genre based on the user's mood.

        For each song, include:
        - title
        - artist
        - album
        - spotify_url

        User mood/genre: {mood}
        """,
        config={
            "response_mime_type": "application/json", # Ensures gemini response is in JSON
            "response_schema": list[Song], # calls the Song class from above to make sure response is structured correctly
        },
    )
# Parse Gemini response into Song objects
    songs: list[Song] = response.parsed
# Get Spotify token to enrich songs with actual Spotify links
    token = get_spotify_token() # get spotify token to search for songs
    for song in songs:
         # Search Spotify for the song using title and artis
        results = search_songs_on_spotify(song.title, song.artist, token)
        # If a valid result is found, update the Spotify URL
        if results and results[0].get('external_url'):
            song.spotify_url = results[0]['external_url']
        else:
            song.spotify_url = 'No spotify link found'


    return songs
