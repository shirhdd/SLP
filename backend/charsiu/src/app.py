import sys
from io import BytesIO
from werkzeug.security import generate_password_hash
from pydub import AudioSegment
import librosa
import numpy as np
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from scipy.io import wavfile
from backend.charsiu.src.Charsiu import charsiu_forced_aligner
import tensorflow as tf
import random
from PIL import Image
from gtts import gTTS
from tensorflow.keras.models import load_model
import pyttsx3
from backend.charsiu.src.phoneme_replacement import Replacer
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import request
from werkzeug.security import check_password_hash

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite for simplicity
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    points = db.Column(db.Integer, default=0)
    avatar = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.points}')"


with app.app_context():
    db.create_all()


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401


@app.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [
        {'username': user.username, 'email': user.email, 'points': user.points,
         'avatar': user.avatar}
        for user in users
    ]
    return jsonify(users_list)


@app.route('/info', methods=['GET'])
def info():
    project_info = {
        "title": "SLP Helper",
        "description": (
            "Welcome to SLP Helper! This application is designed to assist kids and "
            "individuals in improving their Speech-Language Pathology (SLP) status. "
            "Our app allows users to pronounce words and checks if the words are "
            "pronounced correctly at the phoneme level. "
            "Itay and Shir are the developers of this project, both are Electronic "
            "Engineers and Computer Science students at the Hebrew University."
        ),
        "developers": [
            {"name": "Shir Hadad"},
            {"name": "Itay Yamin"}
        ]
    }
    return jsonify(project_info)


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    avatar = data.get('avatar')

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = User(username=username, email=email, password=hashed_password,
                    avatar=avatar)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'}), 201


@app.route('/get_username', methods=['GET'])
def get_username():
    email = request.args.get('email')

    if email is None:
        return jsonify({'error': 'Email parameter is missing'}), 400

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'username': user.username}), 200


phoneme_classification_model = load_model(
    r'C:\Users\shirh\PycharmProjects\SLP\backend\samples\4-s-sh-w-r-11_phonemes_22_epoches.h5')

THRESHOLD = 75

phoneme_alignment_model = charsiu_forced_aligner(
    aligner='charsiu/en_w2v2_fc_10ms')


def write_file_16k(file):
    # Load the audio file
    original_sample_rate, audio = wavfile.read(file)
    output_filename = os.path.join(
        r'C:\Users\inbal\Desktop\SLP\backend\charsiu\src\files',
        'user_wav_processed.wav')
    wavfile.write(output_filename, 16000, audio)


def preprocess(wav):
    wav = wav[:1600]
    zero_padding = tf.zeros([1600] - tf.shape(wav), dtype=tf.float32)
    wav = tf.concat([zero_padding, wav], 0)
    # todo: play with this!
    spectrogram = tf.signal.stft(wav, frame_length=80, frame_step=8)
    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.expand_dims(spectrogram, axis=2)
    return spectrogram


# arr = ["s", "sh", "r", "w", "l", "f", "p", "th", "d", "t", "y"]
arr = ["s", "sh", "r", "w", "l", "f", "p"]


def load_file():
    # Load the audio file
    data, sample_rate = librosa.load('processed_.wav', sr=16000)
    # Convert the NumPy array to a TensorFlow tensor
    wav = tf.convert_to_tensor(data, dtype=tf.float32)
    return wav


def process_file(alignment):
    audio = load_file()
    start, end, phoneme = alignment[0][1]
    audio_cut = audio[int(16000 * start): int(16000 * end)]
    return audio_cut


def create_spectrogram(audio_cut):
    spectrogram = preprocess(audio_cut)
    spectrogram = np.expand_dims(spectrogram, axis=0)
    return spectrogram


def build_json_response(predictions, letter: str):
    predictions = np.round(predictions[0] * 100).astype(
        int)  # Sort indices based on values in descending order to easily access top phonemes
    sorted_indices = np.argsort(-predictions)
    print(predictions)

    # Extract the top two phonemes and their scores
    top_phoneme = arr[sorted_indices[0]]
    top_score = predictions[sorted_indices[0]]

    response = {
        'phonemes': [
            f"Your {top_phoneme} pronunciation gets a {top_score} score"]
    }

    # Check if second top phoneme's score is above 30%
    second_top_phoneme = arr[sorted_indices[1]]
    second_top_score = predictions[sorted_indices[1]]
    if second_top_score > 30:
        response['phonemes'].append(
            f"Your {second_top_phoneme} pronunciation gets a {second_top_score} score")

    if top_score >= THRESHOLD and top_phoneme == letter:
        # When the top score is above the threshold, include a successful message
        response['message'] = "Great job!"
    else:
        # When the top score is below the threshold, include an encouragement message
        response[
            'message'] = f'Come on, you can do better! notice your {letter} pronunciation'

    return jsonify(response), 200


# def text_to_speech(text, output_path):
#     # Initialize the text-to-speech engine
#     engine = pyttsx3.init()
#
#     # Save the speech to a WAV file
#     engine.save_to_file(text, output_path)
#     engine.runAndWait()
#
#     # Load the saved audio file
#     audio = AudioSegment.from_wav(output_path)
#
#     # Set the desired sample rate (16000 Hz)
#     desired_sample_rate = 16000
#
#     # Resample the audio to the desired sample rate
#     resampled_audio = audio.set_frame_rate(desired_sample_rate)
#
#     # Expo the resampled audio to the same file
#     resampled_audio.export(output_path, format="wav")
#
#     print(f"Audio saved successfully at {output_path} with sample rate of 16000 Hz.")


# def gen_correct_wav(word):
#     perfect_file = os.path.join(r'C:\Users\inbal\Desktop\SLP\backend\samples\results', word + "_robot.wav")
#     text_to_speech(word, perfect_file)
#     align_record = phoneme_alignment_model.align(audio='processed_.wav',
#                                                  text=word)
#     align_record = [interval for interval in align_record[0] if interval[2] != '[SIL]']
#     align_perfect = phoneme_alignment_model.align(audio=perfect_file,
#                                                   text=word)
#     align_perfect = [interval for interval in align_perfect[0] if interval[2] != '[SIL]']
#
#     print("1")
#     for_inject = transform_intervals([align_perfect[0], align_record[0]])
#     print("2")
#     # phoneme_firsts = [tuples_to_dictionary(align_perfect[0])[1],
#     #                   tuples_to_dictionary(align_record[0])[1]]
#     # phoneme_intervals = [int(value) for dic in phoneme_firsts for value in
#     #                      dic.values()]
#     modified_wav = inject_phoneme(perfect_file, for_inject)
#     print("3")
#     print(isinstance(modified_wav, AudioSegment))
#     if isinstance(modified_wav, AudioSegment):
#         # Export the modified WAV file
#         output_file = os.path.join(r'C:\Users\inbal\Desktop\SLP\backend\samples\results', 'modified_correct.wav')
#         modified_wav.export(output_file, format="wav")
#         print("modified_wav was saved!")
#     else:
#         raise TypeError("The 'inject_phoneme' function must return a pydub AudioSegment object")
#

# def transform_intervals(input_intervals):
#     transformed_intervals = []
#
#     for start, end, phoneme in input_intervals:
#         transformed_intervals.append((start, end))
#         transformed_intervals.append(phoneme)
#
#     return transformed_intervals


# def tuples_to_dictionary(tuples_list):
#     result_dict = {}
#
#     for start, end, phoneme in tuples_list:
#         result_dict[(start, end)] = phoneme
#
#     return result_dict


# def textGridToJson(textgrid_content):
#     lines = textgrid_content.split('\n')
#
#     phoneme_dict = {}
#
#     start_index = lines.index("5") + 1
#
#     i = start_index  # Start from the line after "5"
#     while i < len(lines) and "IntervalTier" not in lines[i]:
#         start_time = float(lines[i])
#         end_time = float(lines[i + 1])
#         phoneme = lines[i + 2].strip('"')
#         phoneme_dict[(start_time, end_time)] = phoneme
#
#         i += 3  # Move to the next set of phoneme information
#
#     print(phoneme_dict)
#     return phoneme_dict


# def inject_phoneme(perfect_file, phoneme_intervals):
#     """
#      This function extracts the phoneme segment from the first WAV
#       file based on the specified intervals and inserts it into the second WAV
#       file at the specified insertion point.
#      """
#     perfect_wav = AudioSegment.from_file(perfect_file,
#                                          format="wav")
#
#     recorded_wav = AudioSegment.from_file("processed_.wav", format="wav")
#
#     extracted_phoneme = AudioSegment.silent(duration=0)
#
#     for interval, _, _, _ in phoneme_intervals:
#         start_time, end_time = interval
#         extracted_phoneme += perfect_wav[start_time * 1000:end_time * 1000]
#
#     _, _, insert_interval, _ = phoneme_intervals[0]
#     insert_start, insert_end = insert_interval
#
#     modified_second_wav = recorded_wav[
#                           :insert_start * 1000] + extracted_phoneme + recorded_wav[
#                                                                       insert_end * 1000:]
#
#     return modified_second_wav

@app.route('/get_points', methods=['GET'])
def get_points():
    email = request.args.get('email')

    if email is None:
        return jsonify({'error': 'Email parameter is missing'}), 400

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'points': user.points}), 200


@app.route('/update_points', methods=['POST'])
def update_points():
    data = request.get_json()
    email = data.get('email')

    points_to_add = data.get('points')

    if email is None or points_to_add is None:
        return jsonify({'error': 'Email or points parameter is missing'}), 400

    try:
        points_to_add = int(points_to_add)
    except ValueError:
        return jsonify({'error': 'Points parameter must be an integer'}), 400

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    user.points += points_to_add
    db.session.commit()

    return jsonify(
        {'message': 'Points updated successfully', 'points': user.points}), 200


@app.route('/get_correct_pronunciation', methods=['GET'])
def get_correct_pronunciation():
    # Get the word from the query parameter
    word = request.args.get('word', default='default_word', type=str)

    # Generate speech
    tts = gTTS(text=word, lang='en')
    tts.save("word.mp3")  # Save the file temporarily

    # Return the file
    return send_file("word.mp3", as_attachment=True)


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    word = request.form.get('word')

    if word is None:
        return 'Word parameter not provided', 400

    if file and file.filename.endswith('.wav'):
        try:
            write_file_16k(file)
            alignment = phoneme_alignment_model.align(audio='processed_.wav',
                                                      text=word)
            audio_cut = process_file(alignment)
            spectrogram = create_spectrogram(audio_cut)
            predictions = phoneme_classification_model.predict(spectrogram)
            response = build_json_response(predictions, word[0])
            return response

        except Exception as e:
            return jsonify(
                {'error': 'Failed to process file', 'details': str(e)}), 500
    else:
        return None, jsonify({'error': 'Invalid file format'}), 400


@app.route('/speech_inpainting', methods=['GET'])
def speech_inpainting():
    word = request.args.get('word')  # Use request.args for GET parameters

    if word is None:
        return 'Word parameter not provided', 400

    artificial_wav_path = os.path.join(
        r'C:\Users\inbal\Desktop\SLP\backend\charsiu\src\files',
        'artificial-' + word + '.wav')
    user_wav_path = r'C:\Users\inbal\Desktop\SLP\backend\samples\s-sh-wav\shing-6.wav'
    replacer = Replacer(phoneme_alignment_model, phoneme_classification_model,
                        "sing", artificial_wav_path,
                        user_wav_path)
    replacer.generate_artificial_wav()
    output_filename = os.path.join(
        r'C:\Users\inbal\Desktop\SLP\backend\charsiu\src\files',
        'user_wav_processed.wav')
    user_alignment = replacer.aligner(output_filename)
    artificial_alignment = replacer.aligner(artificial_wav_path)

    idx = replacer.identify_error_v1(user_alignment, artificial_alignment)
    replacer.replace(user_alignment, artificial_alignment, idx, 16000)
    fix_wav_path = os.path.join(
        r'C:\Users\inbal\Desktop\SLP\backend\charsiu\src\files',
        'fix.wav')
    return send_file(fix_wav_path, as_attachment=True)


# @app.route('/predict', methods=['POST'])
# def predict():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
#
#     file = request.files['file']
#
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
#
#     word = request.form.get('word')
#
#     if word is None:
#         return 'Word parameter not provided', 400
#
#     if file and file.filename.endswith('.wav'):
#         try:
#             write_file_16k(file)
#             filename_without_extension = os.path.splitext(file.filename)[0]
#             alignment = phoneme_alignment_model.align(audio='processed_.wav',
#                                                       text=filename_without_extension)
#             audio_cut = process_file(alignment)
#             spectrogram = create_spectrogram(audio_cut)
#             predictions = phoneme_classification_model.predict(spectrogram)
#             response = build_json_response(predictions, word[0])
#             gen_correct_wav(word)
#             # return response
#             return send_file('modified_correct',
#                              mimetype='audio/wav'), response
#         except Exception as e:
#             return jsonify(
#                 {'error': 'Failed to process file', 'details': str(e)}), 500
#     else:
#         return None, jsonify({'error': 'Invalid file format'}), 400


# Route for returning a random word
@app.route('/random_word', methods=['GET'])
def random_word():
    words = ['fight', 'thing', 'white']
    word = random.choice(words)
    return jsonify({'word': f'{word}'}), 200


@app.route('/random_words', methods=['GET'])  # Updated endpoint name
def random_words():
    words = ['fight', 'thing', 'white', 'write', 'sing', 'right', 'light']
    # words = ['sing','sing','sing','sing','sing','sing','sing','sing','sing','sing','sing']
    selected_words = random.sample(words,
                                   min(len(words), 5))  # Safely select 4 words
    return jsonify({'words': selected_words}), 200


def build_path(image_name):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the images directory
    image_dir = os.path.join(root_dir, 'resources', 'images')

    # Construct the full path to the image
    image_path = os.path.join(image_dir, image_name + '.jpg')
    print(image_path)
    with Image.open(image_path) as img:
        img.show()

    return image_path


@app.route('/get_image', methods=['GET'])
def get_image():
    image_name = request.args.get('name')
    if image_name is None:
        return 'Please provide the image_name parameter', 400
    image_path = os.path.join('../resources/images', image_name, 'jpeg')
    image_path = f"C:\\Users\\inbal\\Desktop\\SLP\\backend\\resources\\images\\{image_name}.jpg"
    if not os.path.exists(image_path):
        return 'Image not found', 404
    print(image_path)
    return send_file(image_path, mimetype='image/jpg')


@app.route('/get_sound', methods=['GET'])
def upload_sound():
    sound_name = request.args.get('name')
    if sound_name is None:
        return 'Please provide the sound_name parameter', 400
    sound_path = os.path.join('../resources/images', sound_name, '.mp3')
    if not os.path.exists(sound_path):
        return 'Sound File not found', 404

    return send_file(sound_path, as_attachment=True,
                     attachment_filename=sound_name)


# def generate_speech(word, filename='speech.wav'):
#     tts = gTTS(text=word, lang='en')
#     tts.save(filename)
#     return filename


# @app.route('/generate_speech', methods=['GET'])
# def generate_speech_route():
#     if 'word' not in request.args:
#         return 'Word parameter is missing', 400
#
#     word = request.args['word']
#     filename = generate_speech(word)
#
#     # Return the generated WAV file
#     return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
