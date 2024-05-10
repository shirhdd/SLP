import sys
from pydub import AudioSegment
import librosa
import numpy as np
from flask import Flask, request, jsonify, send_file
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

phoneme_alignment_model = charsiu_forced_aligner(
    aligner='charsiu/en_w2v2_fc_10ms')


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


def gen_correct_wav(word):
    perfect_file = os.path.join('../samples/audio/', word, ".wav")
    align_record = phoneme_alignment_model.align(audio='processed_.wav',
                                                 text=word)
    align_perfect = phoneme_alignment_model.align(audio=perfect_file,
                                                  text=word)

    phoneme_firsts = [textGridToJson(align_perfect)[1],
                      textGridToJson(align_record)[1]]
    phoneme_intervals = [int(value) for dic in phoneme_firsts for value in
                         dic.values()]
    modified_wav = inject_phoneme(perfect_file, phoneme_intervals)
    modified_wav.export(
        f'../samples/results/modified_correct.wav',
        format="wav")


def textGridToJson(textgrid_content):
    lines = textgrid_content.split('\n')

    phoneme_dict = {}

    start_index = lines.index("5") + 1

    i = start_index  # Start from the line after "5"
    while i < len(lines) and "IntervalTier" not in lines[i]:
        start_time = float(lines[i])
        end_time = float(lines[i + 1])
        phoneme = lines[i + 2].strip('"')
        phoneme_dict[(start_time, end_time)] = phoneme

        i += 3  # Move to the next set of phoneme information

    print(phoneme_dict)
    return phoneme_dict


def inject_phoneme(perfect_file, phoneme_intervals):
    """
     This function extracts the phoneme segment from the first WAV
      file based on the specified intervals and inserts it into the second WAV
      file at the specified insertion point.
     """
    perfect_wav = AudioSegment.from_file(perfect_file,
                                         format="wav")

    recorded_wav = AudioSegment.from_file("processed_.wav", format="wav")

    extracted_phoneme = AudioSegment.silent(duration=0)

    for interval, _, _, _ in phoneme_intervals:
        start_time, end_time = interval
        extracted_phoneme += perfect_wav[start_time * 1000:end_time * 1000]

    _, _, insert_interval, _ = phoneme_intervals[0]
    insert_start, insert_end = insert_interval

    modified_second_wav = recorded_wav[
                          :insert_start * 1000] + extracted_phoneme + recorded_wav[
                                                                      insert_end * 1000:]

    return modified_second_wav


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
            filename_without_extension = os.path.splitext(file.filename)[0]
            alignment = phoneme_alignment_model.align(audio='processed_.wav',
                                                      text=filename_without_extension)
            audio_cut = process_file(alignment)
            spectrogram = create_spectrogram(audio_cut)
            predictions = phoneme_classification_model.predict(spectrogram)
            response = build_json_response(predictions, word[0])
            gen_correct_wav(word)
            return send_file(f'../samples/results/modified_correct.wav',
                             mimetype='audio/wav'), response
        except Exception as e:
            return jsonify(
                {'error': 'Failed to process file', 'details': str(e)}), 500
    else:
        return None, jsonify({'error': 'Invalid file format'}), 400


# Route for returning a random word
@app.route('/random_word', methods=['GET'])
def random_word():
    words = ['sing', 'song']
    word = random.choice(words)
    return jsonify({'word': f'{word}'}), 200


@app.route('/get_image', methods=['GET'])
def get_image():
    image_name = request.args.get('name')
    if image_name is None:
        return 'Please provide the image_name parameter', 400

    image_path = os.path.join('../resources/images', image_name, 'jpg')
    if not os.path.exists(image_path):
        return 'Image not found', 404

    return send_file(image_path, mimetype='image/jpeg')


@app.route('/get_sound', methods=['GET'])
def upload_sound():
    # Check if the request contains a file
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
