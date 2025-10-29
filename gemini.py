from google import genai
from pydantic import BaseModel
import os
from spotify_service import get_spotify_token, search_songs_on_spotify

class Song(BaseModel): # creates a structure for geminis JSON response
    title: str
    artist: str
    album: str
    spotify_url: str


GOOGLE_API_KEY = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=GOOGLE_API_KEY)

def get_songs(mood: str):
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
    print(response.text)


    songs: list[Song] = response.parsed

    token = get_spotify_token() # get spotify token to search for songs
    for song in songs:
        results = search_songs_on_spotify(song.title, song.artist, token)
        if results and results[0].get('external_url'):
            song.spotify_url = results[0]['external_url']
        else:
            song.spotify_url = 'No spotify link found'


    return songs
