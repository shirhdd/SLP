import glob
import os

import numpy as np
from scipy.io import wavfile
from sklearn import preprocessing
import librosa

from data_preprocessing.data_visualization.utils import mfcc_spectrogram_creation
from data_preprocessing.phonemes.const import TIMIT_TRAIN_FOLDER_PATH, PHONEME_REPRESENTATION_ARRAY_LENGTH, \
    PADDING_IN_SAMPLES, PHONEME_WORKING_SET, TIMIT_DEFAULT_SR, PROCESSED_TRAIN_FOLDER_PATH, \
    NPY_PROCESSED_FOLDER_PATH_TRAIN


def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders


def audio_phoneme_annotations(file_path):
    phoneme_file = []
    for file in file_path:
        file_phn = file + '.phn'
        phoneme_annotations = []
        with open(file_phn, 'r') as phn_file:
            for line in phn_file:
                start_time, end_time, phoneme_label = line.strip().split()
                phoneme_annotations.append((float(start_time), float(end_time), phoneme_label))
        phoneme_file.append((file, phoneme_annotations))
    return phoneme_file


def split_audio(audio_file_phoneme):
    file_path_without_end = audio_file_phoneme[0]
    file_phoneme = audio_file_phoneme[1]
    y, sr = librosa.load(file_path_without_end + '.wav', sr=16000)

    for phoneme in file_phoneme:
        start_time, end_time, ph = phoneme
        if ph in PHONEME_WORKING_SET:
            start_sample = int(max(start_time - PADDING_IN_SAMPLES, 0))
            end_sample = int(min(end_time + PADDING_IN_SAMPLES, file_phoneme[-1][1]))
            librosa.feature.melspectrogram(y=y, sr=sr)
            # Extract the desired portion
            portion = y[start_sample:end_sample]

            if len(portion) < PHONEME_REPRESENTATION_ARRAY_LENGTH:
                # Calculate the number of zeros to add on both sides
                zeros_to_add = PHONEME_REPRESENTATION_ARRAY_LENGTH - len(portion)

                # Distribute the zeros evenly on both sides
                left_zeros = zeros_to_add // 2
                right_zeros = zeros_to_add - left_zeros

                # Add zeros to the left and right sides of the portion
                portion = np.pad(portion, (left_zeros, right_zeros), 'constant')
            elif len(portion) > PHONEME_REPRESENTATION_ARRAY_LENGTH:
                # Calculate how much to truncate from both sides
                excess_length = len(portion) - PHONEME_REPRESENTATION_ARRAY_LENGTH
                left_truncate = excess_length // 2
                right_truncate = excess_length - left_truncate

                # Truncate the portion from both sides to make it 2500 samples long
                portion = portion[left_truncate:-right_truncate]

            # Define the path for the new WAV file
            # Define the folder path for the new WAV file
            folder_path = os.path.join(PROCESSED_TRAIN_FOLDER_PATH, ph)

            # Create the folder if it doesn't exist
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Count the number of files in the folder
            num_files = len(os.listdir(folder_path))

            # Generate the new file name
            new_file_name = f'{ph}@{num_files + 1}.wav'

            mfcc = mfcc_spectrogram_creation(y=portion, sr=TIMIT_DEFAULT_SR)

            # Center MFCC coefficient dimensions to the mean and unit variance
            mfcc = preprocessing.scale(mfcc, axis=1)

            phoneme_wav_numpy_representation.append(portion)
            phoneme_mfcc_numpy_representation.append(mfcc)
            phoneme_tag_representation.append(ph)

            # Define the path for the new WAV file
            new_file_path = os.path.join(folder_path, new_file_name)

            # Save the portion as a WAV file using scipy

            # todo: in order to save the new wav this should be uncmment
            # wavfile.write(new_file_path, sr, portion)


def get_wav_names(folder_path):
    """
    final folder without sub folder inside
    """
    # Create an empty list to store the file names
    wav_files = glob.glob(folder_path + '/*.wav')
    wav_file_names = []
    for wav_file in wav_files:
        # Get only the file name without the full path
        file_name = wav_file
        file_name_without_extension = os.path.splitext(file_name)[0]
        wav_file_names.append(file_name_without_extension)
    filtered_file_names = [file_name for file_name in wav_file_names if "WAV" not in file_name]
    return filtered_file_names


def search_driver():
    sub_dir = fast_scandir(TIMIT_TRAIN_FOLDER_PATH)
    for dir_path in sub_dir:
        print(f"finish dir {dir_path}")
        phoneme_annotations = audio_phoneme_annotations(get_wav_names(dir_path))
        for audio_file_phoneme in phoneme_annotations:
            split_audio(audio_file_phoneme)
    return phoneme_wav_numpy_representation, phoneme_tag_representation , phoneme_mfcc_numpy_representation


phoneme_mfcc_numpy_representation = []
phoneme_tag_representation = []
phoneme_wav_numpy_representation = []
