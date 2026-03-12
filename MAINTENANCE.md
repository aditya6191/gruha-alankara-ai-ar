# Gruha Alankara Maintenance Guide

## Architecture Overview
Gruha Alankara is an Augmented Reality and Agentic AI interior design platform, powered locally by a Python/Flask stack. 

### Core Components
- **Framework:** Flask (Python) rendering Jinja2 HTML templates.
- **Frontend Stack:** HTML5, pure CSS (Custom Dark Theme), Vanilla JavaScript.
- **AR Component:** Leverages `navigator.mediaDevices` WebRTC for local camera overlays on `/preview`.
- **AI Core (`ai_services`):**
    - `assistant.py`: LangChain-powered conversational memory routing.
    - `cache.py`: LRU memory caching for LangChain prompts.
    - `design_generator.py`: HuggingFace/Transformers model bindings (Simulated Granit calls).
    - `image_processor.py`: Pillow (PIL) for sanitizing room camera snaps.
    - `voice.py`: Google TTS enabling multilingual (Telugu, English, Hindi) outputs.
- **Data Layer:** Local `SQLite` managed via SQLAlchemy (`models.py`).
- **Server:** Waitress natively processing WSGI requests.

---

## Local Deployment Instructions

Assuming a generic Windows development environment:

1. **Clone & Setup Environment:**
   ```powershell
   cd \path\to\workspace
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
   *Note: Waitress, Flask, SQLAlchemy, Pillow, gTTS, and LangChain are required.*

3. **Initialize the Database Mock Data:**
   The SQLite relational structure must have initial furniture options to support testing of the auto-booking logic.
   ```powershell
   python init_db_data.py
   ```

4. **Launch the Production Server:**
   Bypass `flask run` debugging mode and launch Waitress:
   ```powershell
   python wsgi.py
   ```
   *The platform is now available locally at `http://127.0.0.1:8080`*

---

## Monitoring and Logs

All HTTP and application-level exceptions (500/404) are gracefully intercepted. Raw output from these errors is safely serialized and written to:
`logs/gruha_alankara.log`

If AI audio fails to render or image processing hits memory halts, developers should check this text file first to identify the point of failure.

---

## Future Extensibility

To scale Gruha Alankara beyond a local mockup:
1. **Migrate Database:** Update `config.py` to point `SQLALCHEMY_DATABASE_URI` away from SQLite (`sqlite:///...`) towards a production PostgreSQL or MongoDB instance.
2. **Dedicated NLP endpoints:** Convert the stubbed Transformers integration in `design_generator.py` into asynchronous REST calls polling a dedicated GPU cloud endpoint.
3. **Session Secret:** Establish a true cryptographically sound token string inside `config.py`.
