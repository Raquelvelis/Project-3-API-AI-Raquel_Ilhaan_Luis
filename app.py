from flask import Flask, render_template, request  # NOT the same as requests
from gemini import get_songs

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/get_mood')
def get_user_info():
    # get gemini from gemini api and display on new page
    mood = request.args.get('Mood')
    songs = get_songs(mood)
    return render_template('gemini.html', user_mood=mood, user_songs=songs)

if __name__ == '__main__':
    app.run()