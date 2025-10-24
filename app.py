import os

from flask import Flask, render_template, request  # NOT the same as requests
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

GOOGLE_API_KEY = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)


@app.route('/get_mood')
def get_user_info():
    # get gemini from gemini api and display on new page
    mood = request.args.get('Mood')
    songs = get_songs(mood)
    return render_template('gemini.html', user_mood=mood, user_songs=songs)

def get_songs(mood):
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    response = model.generate_content(
        f"""You are Moodify, you will recommend 5 songs based on the users mood, if the user specifies a genre,
        then do 5 songs within that genre, if the user does not specify the genre then suggest 5 songs of a random genre based on the users mood. : {mood}"""
    )
    return response.text


if __name__ == '__main__':
    app.run()