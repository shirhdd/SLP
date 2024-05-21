import librosa
import numpy as np
import tensorflow as tf


class ReplaceUtils:
    @staticmethod
    def load_file(file_path):
        # Load the audio file
        data, sample_rate = librosa.load(file_path, sr=16000)
        # Convert the NumPy array to a TensorFlow tensor
        wav = tf.convert_to_tensor(data, dtype=tf.float32)
        return wav

    @staticmethod
    def process_file(alignment, file_path, phoneme_idx=0):
        audio = ReplaceUtils.load_file(file_path)
        start, end, phoneme = alignment[phoneme_idx]
        audio_cut = audio[int(16000 * start): int(16000 * end)]
        return audio_cut

    @staticmethod
    def preprocess(wav):
        wav = wav[:1600]
        zero_padding = tf.zeros([1600] - tf.shape(wav), dtype=tf.float32)
        wav = tf.concat([zero_padding, wav], 0)
        # todo: play with this!
        spectrogram = tf.signal.stft(wav, frame_length=80, frame_step=8)
        spectrogram = tf.abs(spectrogram)
        spectrogram = tf.expand_dims(spectrogram, axis=2)
        return spectrogram

    @staticmethod
    def create_spectrogram(audio_cut):
        spectrogram = ReplaceUtils.preprocess(audio_cut)
        spectrogram = np.expand_dims(spectrogram, axis=0)
        return spectrogram
