import json

import librosa
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from keras import layers
from keras import models
from tensorflow.keras.models import save_model, load_model
from backend.binary.Preprocessor import Preprocessor

ENVIRONMENT_VAR = r'C:\Users\shirh\Dropbox\My PC (LAPTOP-NNRDF68A)\Documents\BSC\Year 4\Semester H\engineer_1'


class Network:
    def deserialize_element_spec(self, serializable_spec):
        def deserialize_tensor_spec(spec_dict):
            return tf.TensorSpec(shape=spec_dict["shape"],
                                 dtype=spec_dict["dtype"])

        if isinstance(serializable_spec, list):
            return tuple(
                deserialize_tensor_spec(spec) for spec in serializable_spec)
        else:  # Similarly, assuming it's either a list (tuple) or a single spec.
            return deserialize_tensor_spec(serializable_spec)

    def load_element_spec(self):
        with open(fr'{ENVIRONMENT_VAR}\element_spec_saved_r_w.json', 'r') as f:
            loaded_spec_dict = json.load(f)

        element_spec = self.deserialize_element_spec(loaded_spec_dict)
        data = tf.data.experimental.load(fr'{ENVIRONMENT_VAR}\\data_saved_r_w',
                                         element_spec=element_spec)

        print("Total data size:", len(list(data.as_numpy_iterator())))
        return data

    def ploting_graph(self, hist):
        plt.title('Loss')
        plt.plot(hist.history['loss'], 'r')
        plt.plot(hist.history['val_loss'], 'b')
        plt.show()
        plt.title('Precision')
        plt.plot(hist.history['precision'], 'r')
        plt.plot(hist.history['val_precision'], 'b')
        plt.show()
        plt.title('Recall')
        plt.plot(hist.history['recall'], 'r')
        plt.plot(hist.history['val_recall'], 'b')
        plt.show()

    def data_choosing(self, data):
        data = data.take(9675)
        data = data.cache()
        data = data.shuffle(buffer_size=3500)
        data = data.batch(25)
        # data = data.prefetch(8)

        train = data.take(350)
        test = data.skip(350).take(37)
        return train, test

    def model_train(self):
        train, test = self.data_choosing(self.load_element_spec())
        model = models.Sequential()
        # todo: change shape!
        model.add(
            layers.Conv2D(16, (3, 3), activation='relu',
                          input_shape=(191, 65, 1)))
        model.add(layers.Conv2D(16, (3, 3), activation='relu'))
        model.add(layers.Flatten())
        model.add(layers.Dense(128, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))

        model.compile('Adam', loss='BinaryCrossentropy',
                      metrics=[tf.keras.metrics.Recall(),
                               tf.keras.metrics.Precision()])
        hist = model.fit(train, epochs=4, validation_data=test)
        self.ploting_graph(hist)
        save_model(model, r'../samples/model_trained.h5')
        return model, train, test

    def testing(self, model, test):
        X_test, y_test = test.as_numpy_iterator().next()
        yhat = model.predict(X_test)
        yhat = [1 if prediction > 0.5 else 0 for prediction in yhat]
        print(yhat)
        print(y_test)


# net = Network()
# Training model #
# model, train, test = net.model_train()

# Testing #
# net.testing(model, test)

# Show scores #

s_sh_arr = [((0.48, 0.75, 'S'), 'sing-4.wav'),
            ((0.29, 0.52, 'SH'), 'shing-6.wav'),
            ((0.39, 0.59, 'SH'), 'shong-11.wav'),
            ((0.28, 0.46, 'SH'), 'shong-10.wav'),
            ((0.51, 0.78, 'S'), 'sang-2.wav'),
            ((0.56, 0.81, 'SH'), 'shang-5.wav'),
            ((0.45, 0.73, 'S'), 'sing-9.wav'),
            ((0.37, 0.61, 'SH'), 'shong.wav'),
            ((0.61, 0.84, 'S'), 'song-12.wav'),
            ((0.28, 0.45, 'S'), 'sing-13.wav'),
            ((0.84, 1.09, 'S'), 'sang-8.wav'),
            ((0.87, 1.07, 'S'), 'song-7.wav'),
            ((0.76, 1.02, 'S'), 'song-1.wav'),
            ((0.61, 0.92, 'S'), 'sing-3.wav')]


def preprocess(wav):
    wav = wav[:1600]
    zero_padding = tf.zeros([1600] - tf.shape(wav), dtype=tf.float32)
    wav = tf.concat([zero_padding, wav], 0)
    # todo: play with this!
    spectrogram = tf.signal.stft(wav, frame_length=80, frame_step=8)
    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.expand_dims(spectrogram, axis=2)
    return spectrogram


def load_wav_16k_mono(filename):
    # Load the file with Librosa
    data, sample_rate = librosa.load(filename, sr=16000)
    # Convert the NumPy array to a TensorFlow tensor
    wav = tf.convert_to_tensor(data, dtype=tf.float32)
    return wav
import pandas as pd


arr = ["s", "sh", "r", "w", "l", "f", "p", "th", "d", "t", "y"]
model = load_model('C:\\Users\\inbal\\Desktop\\SLP\\backend\\samples\\4-s-sh-w-r-11_phonemes_22_epoches.h5')
for sample in s_sh_arr:
    if sample[1] == 'song-12.wav':
        file_path = f'C:\\Users\\inbal\\Desktop\\SLP\\backend\\samples\\s-sh-wav\\{sample[1]}'
        print(sample[1])
        print(sample[0][0],sample[0][1])
        wav = load_wav_16k_mono(file_path)
        spectogram = preprocess(
            wav=wav[int(sample[0][0] * 16000):int(sample[0][1] * 16000)])
        spectogram = np.expand_dims(spectogram, axis=0)
        predictions = model.predict(spectogram)
        print(f"Probabilities of {sample[0][2]}:")
        print(np.round(predictions[0], 2))
        arg_max = np.argmax(predictions[0])
        print(f"Argmax (index of highest probability): {arg_max} with phoneme: {arr[arg_max]}")
        print("####################################################################")
# # Find the argument of the maximum probability
# arg_max = np.argmax(predictions[0])
# print(f"Argmax (index of highest probability): {arg_max} with phoneme: {arr[arg_max]}")
# print("------------------------------------")
# spectogram, _ = Preprocessor().preprocess(
#     'C:\\Users\\inbal\\Desktop\\SLP\\backend\\r-right.wav', "")
# spectogram = np.expand_dims(spectogram, axis=0)
# predictions = model.predict(spectogram)
#
# # Print each probability up to 2 decimal places
# print("Probabilities of r-right:")
# print(np.round(predictions[0], 2))
#
# # Find the argument of the maximum probability
# arg_max = np.argmax(predictions[0])
# print(f"Argmax (index of highest probability): {arg_max} with phoneme: {arr[arg_max]}")
# print("------------------------------------")
# spectogram, _ = Preprocessor().preprocess(
#     'C:\\Users\\inbal\\Desktop\\SLP\\backend\\th-thing.wav', "")
# spectogram = np.expand_dims(spectogram, axis=0)
# predictions = model.predict(spectogram)
#
# # Print each probability up to 2 decimal places
# print("Probabilities of th-thing:")
# print(np.round(predictions[0], 2))
#
# # Find the argument of the maximum probability
# arg_max = np.argmax(predictions[0])
# print(f"Argmax (index of highest probability): {arg_max} with phoneme: {arr[arg_max]}")
# print("------------------------------------")
# spectogram, _ = Preprocessor().preprocess(
#     'C:\\Users\\inbal\\Desktop\\SLP\\backend\\th-thought.wav', "")
# spectogram = np.expand_dims(spectogram, axis=0)
# predictions = model.predict(spectogram)
#
# # Print each probability up to 2 decimal places
# print("Probabilities of th-thought:")
# print(np.round(predictions[0], 2))
#
# # Find the argument of the maximum probability
# arg_max = np.argmax(predictions[0])
# print(f"Argmax (index of highest probability): {arg_max} with phoneme: {arr[arg_max]}")
# print("------------------------------------")
# spectogram, _ = Preprocessor().preprocess(
#     'C:\\Users\\inbal\\Desktop\\SLP\\backend\\w-write.wav', "")
# spectogram = np.expand_dims(spectogram, axis=0)
# predictions = model.predict(spectogram)
#
# # Print each probability up to 2 decimal places
# print("Probabilities of w-write:")
# print(np.round(predictions[0], 2))
#
# # Find the argument of the maximum probability
# arg_max = np.argmax(predictions[0])
# print(f"Argmax (index of highest probability): {arg_max} with phoneme: {arr[arg_max]}")
# print("------------------------------------")
# spectogram, _ = Preprocessor().preprocess(
#     'C:\\Users\\inbal\\Desktop\\SLP\\backend\\w-white.wav', "")
# spectogram = np.expand_dims(spectogram, axis=0)
# predictions = model.predict(spectogram)
#
# # Print each probability up to 2 decimal places
# print("Probabilities of w-white:")
# print(np.round(predictions[0], 2))
#
# # Find the argument of the maximum probability
# arg_max = np.argmax(predictions[0])
# print(f"Argmax (index of highest probability): {arg_max} with phoneme: {arr[arg_max]}")
# print("------------------------------------")
# spectogram, _ = Preprocessor().preprocess(
#     'C:\\Users\\inbal\\Desktop\\SLP\\backend\\d-dad.wav', "")
# spectogram = np.expand_dims(spectogram, axis=0)
# predictions = model.predict(spectogram)
#
# # Print each probability up to 2 decimal places
# print("Probabilities of d-dad:")
# print(np.round(predictions[0], 2))
#
# # Find the argument of the maximum probability
# arg_max = np.argmax(predictions[0])
# print(f"Argmax (index of highest probability): {arg_max} with phoneme: {arr[arg_max]}")
# print("------------------------------------")
