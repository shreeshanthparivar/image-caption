from flask import Flask, render_template, request, redirect, flash, session, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from transformers import BlipProcessor, BlipForConditionalGeneration
from googletrans import Translator
from gtts import gTTS
from PIL import Image
import os
import sqlite3
import uuid

# App configuration
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'change-me')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

BASE_DIR = app.root_path
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
AUDIO_FOLDER = os.path.join(BASE_DIR, 'static', 'audio')
DB_PATH = os.path.join(BASE_DIR, 'users.db')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Load BLIP model and translator
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
translator = Translator()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


@app.before_first_request
def before_first_request():
    init_db()


def generate_caption(image_path):
    image = Image.open(image_path).convert('RGB')
    inputs = processor(image, return_tensors='pt')
    outputs = model.generate(**inputs)
    return processor.decode(outputs[0], skip_special_tokens=True)


def translate_text(text, lang_code):
    try:
        return translator.translate(text, dest=lang_code).text
    except Exception as e:
        return f"Translation Error: {e}"


def generate_audio(text, lang_code):
    filename = f"{uuid.uuid4().hex}.mp3"
    path = os.path.join(AUDIO_FOLDER, filename)
    try:
        tts = gTTS(text=text, lang=lang_code)
        tts.save(path)
        return url_for('static', filename=f'audio/{filename}')
    except Exception:
        return None


def detect_emotion(text):
    emotions = {
        'happy': ['happy', 'joy', 'delight', 'smile', 'laugh'],
        'sad': ['sad', 'tears', 'cry', 'alone', 'gloom', 'down'],
        'angry': ['angry', 'rage', 'furious', 'mad', 'hate'],
        'fear': ['scared', 'afraid', 'fear', 'terror', 'worried'],
        'surprise': ['wow', 'surprise', 'shocked', 'amazed'],
    }
    text = text.lower()
    for emotion, keywords in emotions.items():
        if any(word in text for word in keywords):
            return emotion.capitalize()
    return 'Neutral'


@app.route('/', methods=['GET', 'POST'])
def index():
    caption = None
    image_url = None
    translations = {}
    audio_paths = {}
    emotion = None

    if request.method == 'POST':
        if 'user_id' not in session:
            flash('Please log in to generate captions.', 'error')
            return redirect(url_for('index'))

        image = request.files.get('image')
        if not image or image.filename == '':
            flash('Please select an image to upload.', 'error')
            return redirect(url_for('index'))

        if not allowed_file(image.filename):
            flash('Unsupported file type. Use PNG, JPG, JPEG, GIF, BMP, or WEBP.', 'error')
            return redirect(url_for('index'))

        filename = secure_filename(image.filename)
        filename = f"{uuid.uuid4().hex}_{filename}"
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(save_path)
        image_url = url_for('static', filename=f'uploads/{filename}')

        caption = generate_caption(save_path)
        emotion = detect_emotion(caption)

        lang_map = {'hi': 'Hindi', 'kn': 'Kannada', 'ml': 'Malayalam'}
        for lang_code, lang_name in lang_map.items():
            translated = translate_text(caption, lang_code)
            translations[lang_name] = translated
            audio_url = generate_audio(translated, lang_code)
            if audio_url:
                audio_paths[lang_name] = audio_url

    return render_template(
        'index.html',
        caption=caption,
        image_url=image_url,
        translations=translations,
        audio_paths=audio_paths,
        emotion=emotion,
    )


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')

    if not username or not email or not password:
        flash('All fields are required for registration.', 'error')
        return redirect(url_for('index'))

    if password != confirm_password:
        flash('Passwords do not match.', 'error')
        return redirect(url_for('index'))

    hashed_password = generate_password_hash(password)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute(
            'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            (username, email, hashed_password),
        )
        conn.commit()
        flash('Registration successful! You can now log in.', 'success')
    except sqlite3.IntegrityError:
        flash('Email already exists. Please log in or use another email.', 'error')
    finally:
        conn.close()

    return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, username, password FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()

    if user and check_password_hash(user[2], password):
        session['user_id'] = user[0]
        session['username'] = user[1]
        flash('Login successful!', 'success')
    else:
        flash('Invalid email or password.', 'error')

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
