# Author: Raquel Velis
# Description: Flask app that handles mood-based song recommendations using Gemini API.
from flask import Flask, render_template, request  # NOT the same as requests
from gemini import get_songs
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def homepage():
     """ Render the homepage with the mood input form."""
    return render_template('index.html')


@app.route('/get_mood')
def get_user_info():
""" Retrieve user's mood from query parameters, get song recommendations from Gemini,
    and render them on the results page.
    Returns:
        HTML page with user's mood and recommended songs.
    """
    # Get mood from query string
    mood = request.args.get('Mood')
    # Call Gemini API to get song recommendations based on mood
    songs = get_songs(mood)
   
   # Render results page with mood and songs
    return render_template('gemini.html', user_mood=mood, user_songs=songs)

if __name__ == '__main__':
    # Run the Flask app locally
    app.run()