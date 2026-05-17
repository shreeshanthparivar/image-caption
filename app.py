from flask import Flask, render_template, request, redirect, flash,session, url_for
from transformers import BlipProcessor, BlipForConditionalGeneration
from googletrans import Translator
from gtts import gTTS
from PIL import Image
import os
import random
import sqlite3


# Initialize
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
AUDIO_FOLDER = 'static/audio'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)
app.secret_key = 'zmdb'  # for flash messages

# Load BLIP
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
translator = Translator()

# Generate caption
def generate_caption(image_path):
    image = Image.open(image_path).convert('RGB')
    inputs = processor(image, return_tensors="pt")
    outputs = model.generate(**inputs)
    return processor.decode(outputs[0], skip_special_tokens=True)

# Translate text
def translate_text(text, lang_code):
    try:
        return translator.translate(text, dest=lang_code).text
    except Exception as e:
        return f"Translation Error: {e}"

# Text-to-speech
def generate_audio(text, lang_code):
    filename = f"{random.randint(1000, 9999)}.mp3"
    path = os.path.join(AUDIO_FOLDER, filename)
    try:
        tts = gTTS(text=text, lang=lang_code)
        tts.save(path)
        return path
    except Exception as e:
        return None

# Basic emotion detection (can be replaced by model)
def detect_emotion(text):
    emotions = {
        "happy": ["happy", "joy", "delight", "smile", "laugh"],
        "sad": ["sad", "tears", "cry", "alone"],
        "angry": ["angry", "rage", "furious", "mad"],
        "fear": ["scared", "afraid", "fear", "terror"],
        "surprise": ["wow", "surprise", "shocked"],
    }
    text = text.lower()
    for emotion, keywords in emotions.items():
        if any(word in text for word in keywords):
            return emotion.capitalize()
    return "Neutral"



# Initialize SQLite DB
def init_db():
    conn = sqlite3.connect('users.db')
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

# Register route
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['cpass']

    # Insert into DB
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        flash('Registration successful!', 'success')
        return redirect('/')
    except sqlite3.IntegrityError:
        flash('Email already exists!', 'error')
        return redirect('/')
    finally:
        conn.close()


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = c.fetchone()
    conn.close()

    if user:
        session['user_id'] = user[0]
        session['username'] = user[1]
        flash('Login successful!', 'success')
        return redirect('/')  # or dashboard page
    else:
        flash('Invalid email or password.', 'error')
        return redirect('/')
    
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect('/')



@app.route('/', methods=['GET', 'POST'])
def index():

    caption = image_url = None
    translations = {}
    audio_paths = {}
    emotion = None

    if request.method == 'POST':
        if 'user_id' not in session:
            flash('Please Login.', 'error')
            return redirect('/')
        if 'image' in request.files:
            img = request.files['image']
            if img.filename != '':
                img_path = os.path.join(UPLOAD_FOLDER, img.filename)
                img.save(img_path)
                image_url = img_path
                caption = generate_caption(img_path)
                emotion = detect_emotion(caption)

                # Translations
                lang_map = {'hi': 'Hindi', 'kn': 'Kannada', 'ml': 'Malayalam'}
                for lang_code, lang_name in lang_map.items():
                    trans_text = translate_text(caption, lang_code)
                    translations[lang_name] = trans_text
                    audio_path = generate_audio(trans_text, lang_code)
                    if audio_path:
                        audio_paths[lang_name] = audio_path

    return render_template('index.html', caption=caption, image_url=image_url,
                           translations=translations, audio_paths=audio_paths,
                           emotion=emotion)



if __name__ == '__main__':
    init_db()
    app.run(debug=True)
