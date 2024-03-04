import os

import numpy as np

from backend.initial_try.data_preprocessing.phonemes.const import NPY_PROCESSED_FOLDER_PATH_TRAIN
from backend.initial_try.data_preprocessing.phonemes.split_phoneme_utils import search_driver

phoneme_wav_numpy_representation, phoneme_tag_representation , phoneme_mfcc_numpy_representation = search_driver()

npy_phoneme_folder = NPY_PROCESSED_FOLDER_PATH_TRAIN

# For phoneme_mfcc_numpy_representation
filename = "phoneme_mfcc_numpy_representation.npy"
full_path = os.path.join(npy_phoneme_folder, filename)
np.save(full_path, phoneme_mfcc_numpy_representation)

# For phoneme_tag_representation
filename = "phoneme_tag_representation.npy"
full_path = os.path.join(npy_phoneme_folder, filename)
np.save(full_path, phoneme_tag_representation)

# For phoneme_wav_numpy_representation
filename = "phoneme_wav_numpy_representation.npy"
full_path = os.path.join(npy_phoneme_folder, filename)
np.save(full_path, phoneme_wav_numpy_representation)