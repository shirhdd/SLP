import sys

from flask import Flask, request, jsonify
import random
from flask_cors import CORS
import os
from scipy.io import wavfile
import resampy

from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

phoneme_classification_model = load_model(
    'C:\\Users\\inbal\\Desktop\\SLP\\backend\\samples\\4-s-sh-w-r-11_phonemes_22_epoches.h5')

# phoneme_alignment_model = charsiu_forced_aligner(aligner='charsiu/en_w2v2_fc_10ms')
# phoneme_alignment_model = Serve()


# Function to perform prediction using a model
def predict_wav(wav_file):
    # Placeholder for prediction logic
    # Implement your prediction logic here
    score = random.uniform(0, 1)  # Placeholder for the predicted score
    return score


# Route for predicting from a WAV file
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.wav'):
        try:
            # Load the audio file
            original_sample_rate, audio = wavfile.read(file)

            # Resample the audio to 16000 Hz
            audio_resampled = resampy.resample(audio, original_sample_rate,
                                               16000)

            # Here you can save the resampled audio or process it further
            # Example: Saving the resampled audio to a new file
            output_filename = 'processed_' + file.filename
            wavfile.write(output_filename, 16000, audio_resampled)
            print("File processed and resampled to 16000 Hz")
            return jsonify(
                {'message': 'File processed and resampled to 16000 Hz',
                 'filename': output_filename}), 200
        except Exception as e:
            return jsonify(
                {'error': 'Failed to process file', 'details': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file format'}), 400


# Route for returning a random word
@app.route('/random_word', methods=['GET'])
def random_word():
    # Placeholder for generating a random word
    words = ['right', "white", 'write', 'light', 'fight']
    random_word = random.choice(words)
    return random_word


# def generate_speech(word, filename='speech.wav'):
#     tts = gTTS(text=word, lang='en')
#     tts.save(filename)
#     return filename


@app.route('/generate_speech', methods=['GET'])
def generate_speech_route():
    if 'word' not in request.args:
        return 'Word parameter is missing', 400


# @app.py.route('/generate_speech', methods=['GET'])
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
