import os
import librosa
import json
import tensorflow as tf

i = 0
ENVIRONMENT_VAR = r'C:\Users\shirh\Dropbox\My PC (LAPTOP-NNRDF68A)\Documents\BSC\Year 4\Semester H\engineer_1'


class Preprocessor:
    def load_wav_16k_mono(self, filename):
        # Load the file with Librosa
        data, sample_rate = librosa.load(filename, sr=16000)
        # Convert the NumPy array to a TensorFlow tensor
        wav = tf.convert_to_tensor(data, dtype=tf.float32)
        return wav

    def load_pos_neg_data(self):
        POS = os.path.join(fr'{ENVIRONMENT_VAR}\ProcessedTimit', 'r')
        NEG = os.path.join(fr'{ENVIRONMENT_VAR}\ProcessedTimit', 'w')

        pos = tf.data.Dataset.list_files(POS + '\*.wav')
        neg = tf.data.Dataset.list_files(NEG + '\*.wav')

        positives = tf.data.Dataset.zip(
            (pos, tf.data.Dataset.from_tensor_slices(tf.ones(len(pos)))))
        # positives = positives.take(2500)
        negatives = tf.data.Dataset.zip(
            (neg, tf.data.Dataset.from_tensor_slices(tf.zeros(len(neg)))))
        data = positives.concatenate(negatives)
        return data

    def preprocess(self, file_path, label):
        global i
        print(i)
        i = i + 1
        wav = self.load_wav_16k_mono(file_path)
        wav = wav[:1600]
        zero_padding = tf.zeros([1600] - tf.shape(wav), dtype=tf.float32)
        wav = tf.concat([zero_padding, wav], 0)
        # todo: play with this!
        spectrogram = tf.signal.stft(wav, frame_length=80, frame_step=8)
        spectrogram = tf.abs(spectrogram)
        spectrogram = tf.expand_dims(spectrogram, axis=2)
        return spectrogram, label

    def serialize_element_spec(self, element_spec):
        def serialize_tensor_spec(tensor_spec):
            return {"shape": tensor_spec.shape.as_list(),
                    "dtype": tensor_spec.dtype.name}

        if isinstance(element_spec, tuple):
            return [serialize_tensor_spec(spec) for spec in element_spec]
        else:  # For simplicity, this assumes element_spec is either a tuple or a single tensor spec.
            return serialize_tensor_spec(element_spec)

    def run_all(self):
        spectrograms = []
        labels = []
        data = self.load_pos_neg_data()
        for file_path, label in data.as_numpy_iterator():
            spectrogram, label = self.preprocess(file_path, label)
            spectrograms.append(spectrogram)
            labels.append(label)

        spectrograms = tf.stack(
            spectrograms)  # This is necessary if spectrograms are not already tensors
        labels = tf.convert_to_tensor(labels, dtype=tf.float32)
        data = tf.data.Dataset.from_tensor_slices((spectrograms, labels))

        tf.data.experimental.save(data, fr'{ENVIRONMENT_VAR}\data_saved_r_w')

        # Assuming `data` is your tf.data.Dataset object
        element_spec = data.element_spec
        serializable_spec = self.serialize_element_spec(element_spec)

        with open(fr'{ENVIRONMENT_VAR}\element_spec_saved_r_w.json', 'w') as f:
            json.dump(serializable_spec, f)


Preprocessor().run_all()
