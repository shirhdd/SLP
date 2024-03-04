from flask import Flask, request, jsonify
import random

app = Flask(__name__)

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
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file:
        # Perform prediction
        score = predict_wav(file)

        # Return the predicted score
        return jsonify({'score': score})

# Route for returning a random word
@app.route('/random_word', methods=['GET'])
def random_word():
    # Placeholder for generating a random word
    words = ['right',"white",'write','light','fight']
    random_word = random.choice(words)
    return random_word

def generate_speech(word, filename='speech.wav'):
    tts = gTTS(text=word, lang='en')
    tts.save(filename)
    return filename

@app.route('/generate_speech', methods=['GET'])
def generate_speech_route():
    if 'word' not in request.args:
        return 'Word parameter is missing', 400

    word = request.args['word']
    filename = generate_speech(word)

    # Return the generated WAV file
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
