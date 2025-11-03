import os
import google.generativeai as genai
from dotenv import load_dotenv

from spotify_service import get_spotify_token, search_songs_on_spotify

load_dotenv()

# Configure Gemini with your API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def get_songs(mood):
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"Suggest five songs that match the mood: {mood}. Include title, artist, and album."
        response = model.generate_content(prompt)

        # Parse the response (assuming it's a list of song descriptions)
        songs_data = response.text.split("\n")
        token = get_spotify_token()
        songs = []

        for line in songs_data:
            if line.strip():
                # Basic parsing — you may need to adjust this based on Gemini's actual response format
                parts = line.split(" - ")
                if len(parts) >= 2:
                    title = parts[0].strip()
                    artist = parts[1].strip()
                    album = parts[2].strip() if len(parts) > 2 else "Unknown"
                    spotify_result = search_songs_on_spotify(title, artist, token)
                    spotify_url = spotify_result[0]["external_url"] if spotify_result else None

                    song = type("Song", (), {
                        "title": title,
                        "artist": artist,
                        "album": album,
                        "spotify_url": spotify_url
                    })()
                    songs.append(song)

        return songs
    except Exception as e:
        print(f"Error in get_songs: {e}")
        return []
