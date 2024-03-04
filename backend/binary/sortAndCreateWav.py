import os
import librosa
import numpy as np
import glob
from scipy.io import wavfile

TIMIT_DEFAULT_SR = 16000
PHONEME_WORKING_SET = {"w", "r"}
ENVIRONMENT_VAR = r'C:\Users\shirh\Dropbox\My PC (LAPTOP-NNRDF68A)\Documents\BSC\Year 4\Semester H\engineer_1'


class ProcessCorpus:
    def __init__(self):
        self.length_r = []
        self.length_w = []

    def process_directory(self, directory):
        """
        Process each directory: find WAV files, read phoneme annotations,
         and split audio based on annotations.
        """
        wav_files = glob.glob(os.path.join(directory,
                                           '*.WAV'))  # Assuming .WAV files are the ones we need
        for wav_file in wav_files:
            base_file_path = os.path.splitext(wav_file)[0]
            phoneme_annotations = self.read_phoneme_annotations(
                base_file_path + '.PHN')
            self.split_audio(base_file_path, phoneme_annotations)

    def read_phoneme_annotations(self, phoneme_file_path):
        """
        Read phoneme annotations from a file.
        """
        phoneme_annotations = []
        with open(phoneme_file_path, 'r') as file:
            for line in file:
                start_time, end_time, phoneme_label = line.strip().split()
                phoneme_annotations.append(
                    (int(start_time), int(end_time), phoneme_label))
        return phoneme_annotations

    def split_audio(self, base_file_path, phoneme_annotations):
        """
        Split the audio file based on the phoneme annotations.
        """
        y, sr = librosa.load(base_file_path + '.WAV', sr=TIMIT_DEFAULT_SR)
        for start_time, end_time, phoneme in phoneme_annotations:
            if phoneme in PHONEME_WORKING_SET:
                if phoneme == "r":
                    self.length_r.append(end_time - start_time)
                else:
                    self.length_w.append(end_time - start_time)
                portion = y[
                          int(start_time):int(
                              end_time)]  # Convert to sample index

                self.save_portion(portion, phoneme, sr)

    def save_portion(self, audio_data, phoneme, sample_rate):
        """
        Save the audio portion to the designated folder.
        """
        folder_path = os.path.join(
            rf'{ENVIRONMENT_VAR}\ProcessedTimit',
            phoneme)
        os.makedirs(folder_path,
                    exist_ok=True)  # No need to check if exists, directly make it with exist_ok=True
        file_path = os.path.join(folder_path,
                                 f'{phoneme}@{len(os.listdir(folder_path)) + 1}.wav')
        # sf.write(file_path, audio_data, sample_rate)
        wavfile.write(file_path, sample_rate, audio_data)

    def process_all_directories(self, root_dir):
        """
        Process all subdirectories within the root directory.
        """
        for subdir, dirs, files in os.walk(root_dir):
            print(subdir)
            self.process_directory(subdir)

    def print_txt_screen(self):
        print(len(self.length_w))
        print(np.mean(self.length_w))
        print(np.max(self.length_w))
        print(np.min(self.length_w))

        print(len(self.length_r))
        print(np.mean(self.length_r))
        print(np.max(self.length_r))
        print(np.min(self.length_r))

        with open('statistics_r_w.txt', 'w') as file:
            file.write(f'Count w: {len(self.length_w)}\n')
            file.write(f'Mean w: {np.mean(self.length_w)}\n')
            file.write(f'Max w: {np.max(self.length_w)}\n')
            file.write(f'Min w: {np.min(self.length_w)}\n')
            file.write(f'Count r: {len(self.length_r)}\n')
            file.write(f'Mean r: {np.mean(self.length_r)}\n')
            file.write(f'Max r: {np.max(self.length_r)}\n')
            file.write(f'Min r: {np.min(self.length_r)}\n')


pc = ProcessCorpus()
pc.process_all_directories(
    rf'{ENVIRONMENT_VAR}\timit\train')
pc.print_txt_screen()
