import sys

import librosa
import numpy as np
from flask import Flask, request, jsonify
import random
from flask_cors import CORS
import os
from scipy.io import wavfile
import resampy
from backend.charsiu.src.Charsiu import charsiu_forced_aligner
import tensorflow as tf
import random

from tensorflow.keras.models import load_model

THRESHOLD = 75

app = Flask(__name__)
CORS(app)

phoneme_classification_model = load_model(
    'C:\\Users\\inbal\\Desktop\\SLP\\backend\\samples\\4-s-sh-w-r-11_phonemes_22_epoches.h5')

phoneme_alignment_model = charsiu_forced_aligner(aligner='charsiu/en_w2v2_fc_10ms')


def write_file_16k(file):
    # Load the audio file
    original_sample_rate, audio = wavfile.read(file)
    output_filename = 'processed_.wav'
    wavfile.write(output_filename, 16000, audio)


# taken from prepreocess network file
def preprocess(wav):
    wav = wav[:1600]
    zero_padding = tf.zeros([1600] - tf.shape(wav), dtype=tf.float32)
    wav = tf.concat([zero_padding, wav], 0)
    # todo: play with this!
    spectrogram = tf.signal.stft(wav, frame_length=80, frame_step=8)
    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.expand_dims(spectrogram, axis=2)
    return spectrogram


arr = ["s", "sh", "r", "w", "l", "f", "p", "th", "d", "t", "y"]


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

# def build_json_response(predictions):
#     print(f"Probabilities of word:")
#     print(np.round(predictions[0], 2))
#     arg_max = np.argmax(predictions[0])
#     print(f"Argmax (index of highest probability): {arg_max} with phoneme: {arr[arg_max]}")
#     print("File processed and resampled to 16000 Hz")
def build_json_response(predictions):
    predictions = np.round(predictions[0] * 100).astype(int)    # Sort indices based on values in descending order to easily access top phonemes
    sorted_indices = np.argsort(-predictions)
    print(predictions)

    # Extract the top two phonemes and their scores
    top_phoneme = arr[sorted_indices[0]]
    top_score = predictions[sorted_indices[0]]

    response = {
        'phonemes': [f"Your {top_phoneme} pronunciation gets a {top_score} score"]
    }

    # Check if second top phoneme's score is above 30%
    second_top_phoneme = arr[sorted_indices[1]]
    second_top_score = predictions[sorted_indices[1]]
    if second_top_score > 30:
        response['phonemes'].append(f"Your {second_top_phoneme} pronunciation gets a {second_top_score} score")

    if top_score >= THRESHOLD and top_phoneme == "s":
        # When the top score is above the threshold, include a successful message
        response['message'] = "Great job!"
    else:
        # When the top score is below the threshold, include an encouragement message
        response['message'] = "Come on, you can do better! notice your S pronunciation"

    return jsonify(response), 200



@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.wav'):
        try:

            write_file_16k(file)
            alignment = phoneme_alignment_model.align(audio='processed_.wav', text='song')
            audio_cut = process_file(alignment)
            spectrogram = create_spectrogram(audio_cut)
            predictions = phoneme_classification_model.predict(spectrogram)
            response = build_json_response(predictions)

            return response
        except Exception as e:
            return jsonify({'error': 'Failed to process file', 'details': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file format'}), 400


# Route for returning a random word
@app.route('/random_word', methods=['GET'])
def random_word():
    words = ['sing', 'song']
    word = random.choice(words)
    return jsonify({'word': f'{word}'}), 200


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
