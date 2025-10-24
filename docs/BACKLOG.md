# Moodify Project Backlog

## Overview
This backlog tracks all tasks for the Moodify project - a Flask-based web application that generates personalized Spotify playlists based on mood using AI.

**Project Repository:** Raquelvelis/Project-3-API-AI-Raquel_Ilhaan_Luis
**Team Members:** Raquel, Ilhaan, Luis

---

## Phase 1: Project Setup 🔧

### 1.1 Setup GitHub repository and team collaboration
**Priority:** High | **Type:** Setup | **Architecture:** Core

**Tasks:**
- [ ] Create GitHub repository 'moodify'
- [ ] Add team members (Ilhaan, Luis) as collaborators
- [ ] Set up branch protection rules (require PR reviews)
- [ ] Create Slack channel and invite instructor
- [ ] Create initial project structure
- [ ] Add .gitignore file (Python template + moodify.db)

**Acceptance Criteria:**
- Repository is created and configured
- All team members have access
- Branch protection enabled
- Slack channel active

---

### 1.2 Configure environment variables and API keys
**Priority:** High | **Type:** Setup | **Architecture:** Core

**Tasks:**
- [ ] Create `.env.example` file with all required variables
- [ ] Document required environment variables:
  - `GEMINI_API_KEY`
  - `SPOTIFY_CLIENT_ID`
  - `SPOTIFY_CLIENT_SECRET`
  - `SECRET_KEY`
  - `DATABASE_URL` (optional)
- [ ] Create `.env` file (not committed to Git)
- [ ] Get Gemini API key from Google AI Studio
- [ ] Get Spotify API credentials from Spotify Developer Dashboard

**Resources:**
- Gemini API: https://makersuite.google.com/app/apikey
- Spotify Developer: https://developer.spotify.com/dashboard

**Acceptance Criteria:**
- .env.example created with all variables
- Team has API keys configured locally

---

### 1.3 Setup Python dependencies and virtual environment
**Priority:** High | **Type:** Setup | **Architecture:** Core

**Tasks:**
- [ ] Create `requirements.txt` with:
  - flask==3.0.0
  - python-dotenv==1.0.0
  - requests==2.31.0
  - google-generativeai==0.3.0
- [ ] Create virtual environment
- [ ] Install dependencies
- [ ] Test basic Flask app runs

**Commands:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Acceptance Criteria:**
- requirements.txt created
- Virtual environment works
- Dependencies install successfully

---

## Phase 2: Database Design 💾

### 2.1 Create data models (Playlist and Song classes)
**Priority:** High | **Type:** Feature | **Architecture:** Persistence

**Tasks:**
- [ ] Create `models.py` with Playlist and Song classes
- [ ] Implement Playlist class attributes: id, mood, activity, comment, created_at
- [ ] Implement Song class attributes: id, playlist_id, title, artist, album, spotify_url, preview_url, image_url
- [ ] Add `to_dict()` methods for JSON conversion
- [ ] Add file header documentation (Author: Raquel Velis)
- [ ] Add docstrings to all classes and methods
- [ ] Add validation methods

**Acceptance Criteria:**
- Classes represent database structure
- Easy to convert to/from dictionaries
- Well documented

---

### 2.2 Implement database service with CRD operations
**Priority:** High | **Type:** Feature | **Architecture:** Persistence

**Tasks:**
- [ ] Create `database.py` with core functions
- [ ] Implement `init_db()` - Creates database tables
- [ ] Implement `save_playlist(mood, activity, songs, comment)` - Insert playlist and songs
- [ ] Implement `get_all_playlists()` - Returns list of all playlists (sorted by date)
- [ ] Implement `get_playlist_by_id(playlist_id)` - Returns playlist with all songs
- [ ] Implement `delete_playlist(playlist_id)` - Deletes playlist and all songs
- [ ] Implement `get_db_connection()` - Helper for connection management
- [ ] Add proper error handling
- [ ] Add docstrings to all functions
- [ ] Prevent SQL injection

**Acceptance Criteria:**
- All CRD operations work correctly
- Proper error handling
- Database connection managed properly
- No SQL injection vulnerabilities

---

## Phase 3: API Services 🔌

### 3.1 Implement Gemini AI service for song recommendations
**Priority:** High | **Type:** Feature | **Architecture:** Service

**Tasks:**
- [ ] Create `ai_service.py` module
- [ ] Implement `get_ai_recommendations(mood, activity=None)` function
- [ ] Implement `parse_ai_response(response_text)` function
- [ ] Add error handling for:
  - Missing API key
  - API request failures
  - Timeout errors
  - Invalid responses
- [ ] Add file header documentation (Author: Raquel Velis)
- [ ] Add docstrings to all functions

**API Documentation:**
- Google Generative AI: https://ai.google.dev/tutorials/python_quickstart

**Acceptance Criteria:**
- Returns list of dicts with 'title' and 'artist' keys
- Handles errors gracefully
- Works with different mood and activity combinations

---

### 3.2 Implement Spotify API service for song search
**Priority:** High | **Type:** Feature | **Architecture:** Service

**Tasks:**
- [ ] Create `spotify_service.py` module
- [ ] Implement `get_spotify_token()` - Authenticates with Spotify
- [ ] Implement `search_songs_on_spotify(title, artist, token)` - Search for songs
- [ ] Add error handling for:
  - Missing credentials
  - Authentication failures
  - Search failures
  - Missing data in response
- [ ] Add file header documentation (Author: Raquel Velis)
- [ ] Add docstrings to all functions

**API Documentation:**
- Spotify Web API: https://developer.spotify.com/documentation/web-api

**Acceptance Criteria:**
- Successfully authenticates with Spotify
- Returns detailed song information
- Handles songs not found gracefully

---

## Phase 4: Flask Application 🌐

### 4.1 Implement main Flask application with all routes
**Priority:** High | **Type:** Feature | **Architecture:** Core

**Tasks:**
- [ ] Create `app.py` with all routes
- [ ] Implement `GET /` - Home page
- [ ] Implement `POST /recommendations` - Process mood and get songs
- [ ] Implement `GET /results` - Display recommendations
- [ ] Implement `POST /save` - Save playlist to database
- [ ] Implement `GET /library` - View all saved playlists
- [ ] Implement `GET /playlist/<id>` - View specific playlist
- [ ] Implement `POST /playlist/<id>/delete` - Delete playlist
- [ ] Add error handlers (404, 500)
- [ ] Add session management
- [ ] Add input validation
- [ ] Integrate AI service
- [ ] Integrate Spotify service
- [ ] Integrate database service
- [ ] Add file header documentation (Author: Raquel Velis)
- [ ] Add docstrings to all functions
- [ ] Initialize database on startup

**Acceptance Criteria:**
- All routes work correctly
- Proper error handling
- Session data persists
- Database operations integrated

---

## Phase 5: Frontend 🎨

### 5.1 Create base HTML template with navigation
**Priority:** Medium | **Type:** Feature | **Architecture:** Web

**Tasks:**
- [ ] Create `templates/base.html`
- [ ] Add navigation bar (Home, My Library)
- [ ] Add logo/title
- [ ] Add main content block
- [ ] Add footer
- [ ] Add CSS and JS links
- [ ] Implement responsive design

**Acceptance Criteria:**
- Navigation works on all pages
- Consistent styling
- Responsive layout

---

### 5.2 Create home page with mood input form
**Priority:** High | **Type:** Feature | **Architecture:** Web

**Tasks:**
- [ ] Create `templates/index.html` extending `base.html`
- [ ] Add mood input field (required)
- [ ] Add activity input field (optional)
- [ ] Add submit button
- [ ] Display example moods/activities
- [ ] Add loading indicator
- [ ] Add error display
- [ ] Implement form validation (JavaScript)
- [ ] Add attractive gradient background
- [ ] Implement centered card layout

**Acceptance Criteria:**
- Clean, modern design
- Form validates input
- Shows loading state during API call
- Displays errors clearly
- Works on mobile devices

---

### 5.3 Create results page with song display and save functionality
**Priority:** High | **Type:** Feature | **Architecture:** Web

**Tasks:**
- [ ] Create `templates/results.html` extending `base.html`
- [ ] Display user's mood and activity
- [ ] Create song cards with:
  - Album artwork
  - Song title
  - Artist name
  - Album name
  - Link to Spotify
  - Preview player (if available)
- [ ] Add save playlist section with:
  - Text area for comment
  - Save button
- [ ] Add 'Search Again' button
- [ ] Implement card grid layout
- [ ] Add hover effects

**Acceptance Criteria:**
- All song information displays correctly
- Images load properly
- Links work
- Save form functional
- Success message on save
- Responsive on all devices

---

### 5.4 Create library page to view all saved playlists
**Priority:** Medium | **Type:** Feature | **Architecture:** Web

**Tasks:**
- [ ] Create `templates/library.html` extending `base.html`
- [ ] Add page title 'My Playlists'
- [ ] Create playlist cards showing:
  - Mood/activity
  - Comment snippet
  - Date created
  - Number of songs
  - 'View' button
  - Album art collage (first 4 songs)
- [ ] Add empty state:
  - Message when no playlists
  - Button to create first playlist
- [ ] Implement grid layout
- [ ] Add hover effects

**Acceptance Criteria:**
- All playlists display correctly
- Cards are clickable
- Empty state shows appropriately
- Sorted by date (newest first)
- Responsive layout

---

### 5.5 Create playlist details page with delete functionality
**Priority:** Medium | **Type:** Feature | **Architecture:** Web

**Tasks:**
- [ ] Create `templates/playlist_details.html` extending `base.html`
- [ ] Add playlist header with:
  - Mood and activity
  - Date created
  - Full comment
- [ ] Display all songs with same layout as results page
- [ ] Add 'Delete Playlist' button with confirmation
- [ ] Add 'Back to Library' button
- [ ] Add 'Create New Playlist' button
- [ ] Implement delete confirmation modal/dialog
- [ ] Add success/error messages

**Acceptance Criteria:**
- All playlist information displays
- Songs display correctly
- Delete works with confirmation
- Navigation buttons work
- Responsive design

---

## Phase 6: Testing 🧪

### 6.1 Write unit tests for all components
**Priority:** High | **Type:** Test | **Architecture:** Core

**Tasks:**
- [ ] Create `test_models.py`:
  - Test Playlist class methods
  - Test Song class methods
  - Test to_dict() conversions
- [ ] Create `test_database.py`:
  - Test init_db() creates tables
  - Test save_playlist()
  - Test get_all_playlists()
  - Test get_playlist_by_id()
  - Test delete_playlist()
  - Test with empty database
  - Use test database (not production)
- [ ] Create `test_ai_service.py`:
  - Test get_ai_recommendations() with valid mood
  - Test with mood and activity
  - Test with empty mood
  - Test with invalid API key
  - Test parse_ai_response()
- [ ] Create `test_spotify_service.py`:
  - Test get_spotify_token() success/failure
  - Test search_songs_on_spotify() with real song
  - Test with non-existent song
- [ ] Create `test_app.py`:
  - Test all routes (GET /, POST /recommendations, etc.)
  - Test error handling
- [ ] Use pytest or unittest
- [ ] Aim for >70% code coverage

**Acceptance Criteria:**
- All tests pass
- Good code coverage
- Tests are maintainable

---

### 6.2 Perform integration testing
**Priority:** Medium | **Type:** Test | **Architecture:** Core

**Tasks:**
- [ ] Test main flow:
  1. Enter mood/activity
  2. Get recommendations
  3. View results
  4. Save playlist with comment
  5. View library
  6. View playlist details
  7. Delete playlist
- [ ] Test error scenarios:
  - Invalid API keys
  - Network failures
  - Empty responses
  - Database errors
- [ ] Test with different moods and activities
- [ ] Test concurrent users (sessions)
- [ ] Document any bugs found

**Acceptance Criteria:**
- Complete flow works end-to-end
- Error handling is robust
- Documentation of test results

---

## Phase 7: Documentation 📚

### 7.1 Create comprehensive README with setup instructions
**Priority:** High | **Type:** Docs | **Architecture:** Core

**Tasks:**
- [ ] Add project description
- [ ] Add features list (including persistence)
- [ ] Add technology stack
- [ ] Add database schema (ER diagram)
- [ ] Add installation instructions
- [ ] Add how to get API keys (step-by-step)
- [ ] Add how to run the application
- [ ] Add how to run tests
- [ ] Add team members and roles
- [ ] Add screenshots (all pages):
  - Home page
  - Results page with save form
  - Library page
  - Playlist details page
  - Example saved playlists
- [ ] Add troubleshooting section

**Acceptance Criteria:**
- Complete and accurate documentation
- All instructions tested on fresh install
- Screenshots included
- Well-formatted

---

### 7.2 Add code documentation and comments
**Priority:** Medium | **Type:** Docs | **Architecture:** Core

**Tasks:**
- [ ] Review and update documentation in all files:
  - app.py
  - ai_service.py
  - spotify_service.py
  - database.py
  - models.py
  - All template files
- [ ] Ensure all files have header comments with Author: Raquel Velis
- [ ] Ensure all functions have docstrings
- [ ] Add inline comments where logic is complex
- [ ] Document database schema in code

**Acceptance Criteria:**
- All code is well-documented
- Docstrings follow Python conventions
- Complex logic is explained

---

### 7.3 Create CITATIONS.md for all resources used
**Priority:** Medium | **Type:** Docs | **Architecture:** Core

**Tasks:**
- [ ] Create `CITATIONS.md` file
- [ ] Document AI tools used (Claude, ChatGPT, Gemini, etc.)
- [ ] Document documentation sites (Flask, Spotify API, Gemini API)
- [ ] Document Stack Overflow answers
- [ ] Document tutorial videos
- [ ] Document database tutorials
- [ ] Document any other external resources

**Format:**
```
## AI Tools
- Claude AI (Anthropic) - Used for code generation and debugging
  - URL: https://claude.ai

## Documentation
- Flask Documentation
  - URL: https://flask.palletsprojects.com/

## Tutorials
- [Tutorial Name] by [Author]
  - URL: [url]
  - Used for: [description]
```

**Acceptance Criteria:**
- All resources documented
- URLs included
- Clear descriptions of how resources were used

---

## Phase 8: Final 🎯

### 8.1 Final review and testing before submission
**Priority:** High | **Type:** Setup | **Architecture:** Core

**Tasks:**
- [ ] **Testing:**
  - Run full test suite
  - Test on fresh Python environment
  - Test database migrations
- [ ] **Documentation:**
  - Review all code has proper documentation
  - Check all links work in README
  - Verify .env.example is complete
- [ ] **Security:**
  - Ensure no API keys in repository
  - Ensure moodify.db not in repository
  - Review .gitignore is complete
- [ ] **Quality:**
  - Code follows Python style guidelines
  - All features work as expected
  - No broken links or images

**Acceptance Criteria:**
- All checks complete
- Ready for submission

---

### 8.2 Prepare presentation and demo
**Priority:** High | **Type:** Docs | **Architecture:** Core

**Tasks:**
- [ ] Create presentation slides
- [ ] Prepare demo script
- [ ] Practice presentation
- [ ] Prepare answers for common questions

**Demo Flow:**
1. Show home page
2. Generate playlist for a mood
3. Display results
4. Save playlist with comment
5. Show library
6. View playlist details
7. Delete playlist

**Talking Points:**
- Architecture overview
- Technology choices
- Challenges faced
- What we learned
- Team collaboration

**Acceptance Criteria:**
- Presentation ready
- Demo works smoothly
- Team is prepared

---

### 8.3 Submit project deliverables
**Priority:** High | **Type:** Setup | **Architecture:** Core

**Tasks:**
- [ ] Create zip file of project (exclude moodify.db and venv)
- [ ] Upload zip to Project 3 dropbox
- [ ] Push final code to GitHub
- [ ] Submit GitHub URL to dropbox
- [ ] Verify submission is complete

**Pre-Submission Checklist:**
- [ ] README.md is complete with screenshots
- [ ] All tests pass
- [ ] No API keys in repository
- [ ] .gitignore is correct
- [ ] CITATIONS.md is complete
- [ ] requirements.txt is up to date

**Acceptance Criteria:**
- Project submitted on time
- All deliverables included
- Submission verified

---

## Label System

The project uses the following labels for organization:

### Architecture Labels
- `architecture:web` - Frontend/Web interface components
- `architecture:service` - API integration services
- `architecture:persistence` - Database and data models
- `architecture:core` - Core Flask application

### Phase Labels
- `phase:setup` - Project setup and configuration
- `phase:database` - Database design and implementation
- `phase:api` - API development
- `phase:frontend` - Frontend development
- `phase:testing` - Testing and quality assurance
- `phase:documentation` - Documentation tasks

### Type Labels
- `type:feature` - New feature implementation
- `type:setup` - Setup and configuration
- `type:test` - Testing related
- `type:docs` - Documentation

### Priority Labels
- `priority:high` - High priority
- `priority:medium` - Medium priority
- `priority:low` - Low priority

---

## Summary Statistics

**Total Tasks:** 22 main issues across 8 phases
**Team Members:** 3 (Raquel Velis, Ilhaan, Luis)
**Architecture Layers:** 4 (Web, Service, Persistence, Core)

**Next Steps:**
1. Visit: https://github.com/Raquelvelis/capstone_project_3/issues
2. Review and assign issues to team members
3. Use project board to track progress
4. Start working on Phase 1 issues