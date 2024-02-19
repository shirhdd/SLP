import os
import librosa
import numpy as np
import soundfile as sf
import glob
from scipy.io import wavfile

TIMIT_DEFAULT_SR = 16000
PHONEME_WORKING_SET = {"w", "r"}
length_r = []
length_w = []


def process_directory(directory):
    """
    Process each directory: find WAV files, read phoneme annotations, and split audio based on annotations.
    """
    wav_files = glob.glob(os.path.join(directory, '*.WAV'))  # Assuming .WAV files are the ones we need
    for wav_file in wav_files:
        base_file_path = os.path.splitext(wav_file)[0]
        phoneme_annotations = read_phoneme_annotations(base_file_path + '.PHN')
        split_audio(base_file_path, phoneme_annotations)


def read_phoneme_annotations(phoneme_file_path):
    """
    Read phoneme annotations from a file.
    """
    phoneme_annotations = []
    with open(phoneme_file_path, 'r') as file:
        for line in file:
            start_time, end_time, phoneme_label = line.strip().split()
            phoneme_annotations.append((int(start_time), int(end_time), phoneme_label))
    return phoneme_annotations


def split_audio(base_file_path, phoneme_annotations):
    """
    Split the audio file based on the phoneme annotations.
    """
    y, sr = librosa.load(base_file_path + '.WAV', sr=TIMIT_DEFAULT_SR)
    for start_time, end_time, phoneme in phoneme_annotations:
        if phoneme in PHONEME_WORKING_SET:
            if phoneme == "r":
                length_r.append(end_time - start_time)
            else:
                length_w.append(end_time - start_time)
            portion = y[int(start_time):int(end_time)]  # Convert to sample index

            save_portion(portion, phoneme, sr)


def save_portion(audio_data, phoneme, sample_rate):
    """
    Save the audio portion to the designated folder.
    """
    folder_path = os.path.join("S:\\ProcessedTimit", phoneme)
    os.makedirs(folder_path, exist_ok=True)  # No need to check if exists, directly make it with exist_ok=True
    file_path = os.path.join(folder_path, f'{phoneme}@{len(os.listdir(folder_path)) + 1}.wav')
    # sf.write(file_path, audio_data, sample_rate)
    wavfile.write(file_path, sample_rate, audio_data)


def process_all_directories(root_dir):
    """
    Process all subdirectories within the root directory.
    """
    for subdir, dirs, files in os.walk(root_dir):
        print(subdir)
        process_directory(subdir)


# Example usage
process_all_directories("S:\\timit\\timit\\train")
print(len(length_w))
print(np.mean(length_w))
print(np.max(length_w))
print(np.min(length_w))

print(len(length_r))
print(np.mean(length_r))
print(np.max(length_r))
print(np.min(length_r))

# with open('statistics.txt', 'w') as file:
#     file.write(f'Count: {len(length)}\n')
#     file.write(f'Mean: {np.mean(length)}\n')
#     file.write(f'Max: {np.max(length)}\n')
#     file.write(f'Min: {np.min(length)}\n')