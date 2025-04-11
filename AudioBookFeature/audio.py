from flask import Blueprint, render_template, send_file, jsonify
from gtts import gTTS
import pandas as pd
import os

# Initialize Blueprint
audiobooks_bp = Blueprint('audiobooks', __name__,
                         template_folder='templates',
                         static_folder='static')

# Get absolute path to current directory
dir_path = os.path.dirname(os.path.abspath(__file__))

# Load audiobook data with absolute path
csv_path = os.path.join(dir_path, 'audio_books.csv')
audiobooks_df = pd.read_csv(csv_path)

@audiobooks_bp.route('/')
def audiobooks():
    books = []
    for _, row in audiobooks_df.iterrows():
        book = row.to_dict()
        audio_path = os.path.join(dir_path, 'static', 'audio', f"{row['BOOK_ID']}.mp3")
        book['audio_exists'] = os.path.exists(audio_path)
        books.append(book)
    return render_template('audiobooks.html', books=books)

@audiobooks_bp.route('/generate_audio/<int:book_id>')
def generate_audio(book_id):
    try:
        book = audiobooks_df[audiobooks_df['BOOK_ID'] == book_id].iloc[0]
        tts = gTTS(text=book['Text'], lang='en')
        
        # Create audio directory if not exists
        audio_dir = os.path.join(dir_path, 'static', 'audio')
        os.makedirs(audio_dir, exist_ok=True)
        
        # Save file
        output_path = os.path.join(audio_dir, f"{book_id}.mp3")
        tts.save(output_path)
        
        return jsonify(success=True)
    
    except IndexError:
        return jsonify(success=False, error="Book not found"), 404
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

@audiobooks_bp.route('/play_audio/<int:book_id>')
def play_audio(book_id):
    audio_path = os.path.join(dir_path, 'static', 'audio', f"{book_id}.mp3")
    return send_file(audio_path)