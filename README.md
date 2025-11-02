# Moodify — AI‑Personalized Spotify Suggestions (Flask)

Moodify is a small Flask web application that combines an AI model (Google Gemini) with the Spotify Web API to recommend songs tailored to a user’s mood or preferred genre. The AI proposes candidate tracks, then the app enriches those results with live Spotify search to provide playable links and metadata.

This repository is an educational team project focused on collaboration, API usage, AI integration, testing, and documentation.


## Team
- Luis Laguna — Frontend, Gemini integration, UI/UX implementation
- Raquel Velis — Backend, repository management, development environment setup, issues management, Spotify API integration
- Ilhaan Mohamed — Documentation


## Objectives (from assignment)
- Work in a team; collaborate using GitHub, branches, pull requests, and code reviews
- Communicate in Slack
- Use public APIs and their documentation
- Embed Gemini AI tools for user personalization
- Track tasks with GitHub Issues
- Persist data (bookmarks), read/edit persistent data
- Manage dependencies
- Design app structure; write modular code
- Write unit tests
- Practice error handling


## Current Status
- Core flow implemented: Mood/genre input → Gemini suggestions → Spotify lookup → Display results
- Flask app and templates in place
- Basic unit/integration tests included for Spotify search logic
- Persistence/bookmarks: not yet implemented (see Roadmap)


## Project Structure
```
app.py                       # Flask app, routes
gemini.py                    # Gemini client: prompt + structured JSON parsing
spotify_service.py           # Spotify auth and search helpers
requirements.txt             # Python dependencies
static/                      # Static assets (CSS, images)
  ├─ style.css
  └─ spotify_logo_2.png
templates/                   # Jinja2 templates
  ├─ index.html              # Home page form (mood/genre)
  └─ gemini.html             # Results page
tests/                       # Unit/integration tests (pytest)
docs/                        # Extra docs (setup, backlog, scripts)
```

Key files worth reading first:
- `app.py` — defines routes `/` and `/get_mood`
- `gemini.py` — function `get_songs(mood)` uses Gemini to propose tracks, then enriches with Spotify links
- `spotify_service.py` — functions `get_spotify_token()` and `search_songs_on_spotify(...)` with defensive parsing


## How it works
1. User enters a mood or a genre on the home page.
2. `gemini.get_songs(mood)` calls Gemini (`gemini-2.5-flash`) to produce a structured JSON list of 5 songs with fields: `title`, `artist`, `album`, `spotify_url`.
3. For each Gemini suggestion, the app performs a Spotify Search to retrieve the canonical track and its `external_url` (Spotify link). If a link is found, it replaces/sets `spotify_url`.
4. Results are rendered on `templates/gemini.html`.


## Getting Started

### Prerequisites
- Python 3.10+
- A Google AI Studio API key for Gemini
- Spotify Developer account with a registered application (Client ID/Secret)

### Local setup
1. Clone the repository
   ```bash
   git clone <your-repo-url>
   cd Project-3-API-AI-Raquel_Ilhaan_Luis
   ```

2. Create and activate a virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # macOS/Linux
   # .\venv\Scripts\activate    # Windows PowerShell
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your credentials
   ```env
   # Google AI (Gemini)
   GEMINI_API_KEY=your_gemini_api_key_here

   # Spotify API (Client Credentials Flow)
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret

   # Optional Flask settings
   FLASK_ENV=development
   ```

5. Run the app
   ```bash
   # Option A: via Flask built‑in server
   python app.py
   # or
   flask --app app run
   ```

6. Open your browser
   - http://127.0.0.1:5000/


## Usage
- Enter a mood (e.g., "happy", "melancholic", "workout") or specify a genre (e.g., "jazz", "house").
- Submit to get 5 AI‑recommended songs. The app attempts to find each track on Spotify and provide a link.


## Testing
We use `pytest` for unit/integration tests.

- Run all tests:
  ```bash
  pytest -q
  ```
- Notable tests:
  - `tests/test_retrieve_five_given_songs.py`
  - `tests/test_integration_search_songs_on_spotify.py`


## Error Handling
- `spotify_service.get_spotify_token()` raises `ValueError` when env vars are missing and `RuntimeError` on non‑200 responses.
- `spotify_service.search_songs_on_spotify()` raises `ValueError` if token is missing and `RuntimeError` if the search fails.
- The Flask route currently surfaces errors directly; future improvement: add graceful error pages and user‑friendly messages.


## Configuration and Secrets
- Secrets are read from `.env` via `python-dotenv`. Do not commit real secrets.
- Environment variables used:
  - `GEMINI_API_KEY`
  - `SPOTIFY_CLIENT_ID`
  - `SPOTIFY_CLIENT_SECRET`
  - Optional: `FLASK_ENV`


## Dependency Management
- All required packages are listed in `requirements.txt`.
- To update dependencies, modify `requirements.txt` and run `pip install -r requirements.txt`.


## Roadmap / Future Work
- Persist user “bookmarked” tracks (database or simple file storage)
- Add user accounts/sessions and saved preferences
- Improve prompt engineering and result validation
- Add pagination and loading states in UI
- Add more tests: Flask route tests, failure paths, and HTML rendering
- Better error pages and logging


## Collaboration Workflow
- Use GitHub Issues to track tasks and bugs
- Create feature branches from `main`
- Open Pull Requests; every PR must be reviewed before merging
- Use the private Slack channel for day‑to‑day coordination
- Keep commit messages clear and atomic

Helpful docs in this repo:
- `docs/EnvironmentSetupGuide.md`
- `docs/BACKLOG.md`

## Citations and Resources
List and link all resources used to develop the project (required by assignment). For example:
- Google AI Studio / Gemini API docs
- Spotify Web API docs
- Flask docs
- Tutorials, websites, videos, AI tools (ChatGPT, Gemini, etc.)

Example template (replace with actual links used):
- Gemini: https://ai.google.dev/gemini-api
- Spotify: https://developer.spotify.com/documentation/web-api
- Flask: https://flask.palletsprojects.com/
- Python‑Dotenv: https://pypi.org/project/python-dotenv/
