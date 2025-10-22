from google import genai
import os 

GOOGLE_API_KEY = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=GOOGLE_API_KEY)

def get_songs(mood):
    response = client.models.generate_content(
    model='gemini-2.5-flash', 
    contents=f"""You are Moodify, you will recommend 5 songs based on the users mood, if the user specifies a genre,
    then do 5 songs within that genre, if the user does not specify the genre then suggest 5 songs of a random genre based on the users mood. : {mood}"""
)
    return response.text


