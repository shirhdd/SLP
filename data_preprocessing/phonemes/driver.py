import os

from data_preprocessing.phonemes.const import TIMIT_TRAIN_FOLDER_PATH
from data_preprocessing.phonemes.utils import fast_scandir, audio_phoneme_annotations, get_wav_names, split_audio


def search_driver():
    sub_dir = fast_scandir(TIMIT_TRAIN_FOLDER_PATH)
    for dir_path in sub_dir:
        print(f"finish dir {dir_path}")
        phoneme_annotations = audio_phoneme_annotations(get_wav_names(dir_path))
        for audio_file_phoneme in phoneme_annotations:
            split_audio(audio_file_phoneme)


# search_driver()
