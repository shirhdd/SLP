import os
import librosa
from matplotlib import pyplot as plt
import tensorflow as tf
import tensorflow_io as tfio

i = 0
def load_wav_16k_mono(filename):
    # Load the file with Librosa
    data, sample_rate = librosa.load(filename, sr=16000)
    # Convert the NumPy array to a TensorFlow tensor
    wav = tf.convert_to_tensor(data, dtype=tf.float32)
    return wav


R = os.path.join('S:\\ProcessedTimit', 'r')
S = os.path.join('S:\\ProcessedTimit', 's')
W = os.path.join('S:\\ProcessedTimit', 'w')
SH = os.path.join('S:\\ProcessedTimit', 'sh')

r = tf.data.Dataset.list_files(R + '\*.wav')
s = tf.data.Dataset.list_files(S + '\*.wav')
w = tf.data.Dataset.list_files(W + '\*.wav')
sh = tf.data.Dataset.list_files(SH + '\*.wav')


r = tf.data.Dataset.zip((r, tf.data.Dataset.from_tensor_slices(tf.cast(tf.ones(len(r)), dtype=tf.float32) * 0)))
s = tf.data.Dataset.zip((s, tf.data.Dataset.from_tensor_slices(tf.cast(tf.ones(len(s)), dtype=tf.float32) * 1)))
w = tf.data.Dataset.zip((w, tf.data.Dataset.from_tensor_slices(tf.cast(tf.ones(len(w)), dtype=tf.float32) * 2)))
sh = tf.data.Dataset.zip((sh, tf.data.Dataset.from_tensor_slices(tf.cast(tf.ones(len(sh)), dtype=tf.float32) * 3)))
data = r.concatenate(s).concatenate(w).concatenate(sh)



def preprocess(file_path, label):
    global i
    print(i)
    i = i + 1
    wav = load_wav_16k_mono(file_path)
    wav = wav[:1600]
    zero_padding = tf.zeros([1600] - tf.shape(wav), dtype=tf.float32)
    wav = tf.concat([zero_padding, wav], 0)
    # todo: play with this!
    spectrogram = tf.signal.stft(wav, frame_length=80, frame_step=8)
    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.expand_dims(spectrogram, axis=2)
    return spectrogram, label

spectrograms  = []
labels  = []
for file_path, label in data.as_numpy_iterator():
    spectrogram, label = preprocess(file_path, label)
    spectrograms.append(spectrogram)
    labels.append(label)

spectrograms = tf.stack(spectrograms)  # This is necessary if spectrograms are not already tensors
labels = tf.convert_to_tensor(labels, dtype=tf.float32)
data = tf.data.Dataset.from_tensor_slices((spectrograms, labels))


tf.data.experimental.save(data, "S:\\data_saved_r_w_s_sh")

import json
import tensorflow as tf

def serialize_element_spec(element_spec):
    def serialize_tensor_spec(tensor_spec):
        return {"shape": tensor_spec.shape.as_list(), "dtype": tensor_spec.dtype.name}

    if isinstance(element_spec, tuple):
        return [serialize_tensor_spec(spec) for spec in element_spec]
    else:  # For simplicity, this assumes element_spec is either a tuple or a single tensor spec.
        return serialize_tensor_spec(element_spec)

# Assuming `data` is your tf.data.Dataset object
element_spec = data.element_spec
serializable_spec = serialize_element_spec(element_spec)

with open('element_spec_saved_r_w_s_sh.json', 'w') as f:
    json.dump(serializable_spec, f)

