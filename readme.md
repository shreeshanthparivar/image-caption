# CaptionGenius

A Flask app that generates captions for uploaded images using BLIP, translates captions into Hindi, Kannada, and Malayalam, generates audio for translations, and detects the caption emotion.

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Run the app:

   ```powershell
   python app.py
   ```

4. Open your browser at `http://127.0.0.1:5000`

## Notes

- The app stores user accounts in `users.db`.
- Uploaded images are saved under `static/uploads`.
- Generated audio files are saved under `static/audio`.
- The database and static files are ignored by `.gitignore`.
