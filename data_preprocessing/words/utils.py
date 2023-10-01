import librosa
from scipy.io import wavfile


def cut_word_by_sample(file_path, start_sample, end_sample, save=False):
    y, sr = librosa.load(file_path, sr=16000)
    y = y[start_sample: end_sample]
    if save:
        wavfile.write("C:\\Users\\itayy\\Desktop\\SLP\\data_preprocessing\\words\\test.wav", int(sr), y)


cut_word_by_sample(start_sample=9230, end_sample=13360,
                   file_path="C:\\Users\\itayy\\Desktop\\engineering_projects\\timit\\train\\dr7\\mdks0\\sx436.wav",
                   save=True)
