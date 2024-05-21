import pyttsx3
import os
from pydub import AudioSegment
from scipy.io import wavfile

from backend.charsiu.src.Charsiu import charsiu_forced_aligner
from backend.charsiu.src.replace_utils import ReplaceUtils
from tensorflow.keras.models import load_model

ALIGNMENT_MATCH = -1
PHONEME_LOC_TUPLE = 2


class Replacer:
    def __init__(self, phoneme_alignment_model, phoneme_classification_model, word, artificial_wav_path, user_wav_path):
        self.phoneme_alignment_model = phoneme_alignment_model
        self.phoneme_classification_model = phoneme_classification_model
        self.word = word
        self.artificial_wav_path = artificial_wav_path
        self.user_wav_path = user_wav_path

    def write_file_16k(self):
        original_sample_rate, audio = wavfile.read(self.user_wav_path)
        output_filename = os.path.join(r'C:\Users\inbal\Desktop\SLP\backend\charsiu\src\files',
                                       'user_wav_processed.wav')
        wavfile.write(output_filename, 16000, audio)

    def generate_artificial_wav(self):
        try:
            engine = pyttsx3.init()

            engine.save_to_file(self.word, self.artificial_wav_path)
            engine.runAndWait()

            audio = AudioSegment.from_wav(self.artificial_wav_path)

            desired_sample_rate = 16000

            resampled_audio = audio.set_frame_rate(desired_sample_rate)

            resampled_audio.export(self.artificial_wav_path, format="wav")
            print("success generate_artificial_wav")
        except Exception as e:
            print(f"An error occurred while creating artificial_wav in function generate_artificial_wav: {e}")

    def aligner(self, path):

        aligned_record = self.phoneme_alignment_model.align(
            audio=path, text=self.word)
        aligned_record = [interval for interval in aligned_record[0] if interval[2] != '[SIL]']

        return aligned_record

    def replace(self, user_alignment, artificial_alignment, idx, sample_rate=16000):
        if idx < 0 or idx >= len(user_alignment) or idx >= len(artificial_alignment):
            raise ValueError("Invalid index or alignment data length")

        user_path_processed = os.path.join(r'C:\Users\inbal\Desktop\SLP\backend\charsiu\src\files',
                                           'user_wav_processed.wav')
        user_audio = AudioSegment.from_wav(
            user_path_processed).set_frame_rate(sample_rate)
        artificial_audio = AudioSegment.from_wav(self.artificial_wav_path).set_frame_rate(sample_rate)

        phoneme_start = int(artificial_alignment[idx][0] * 1000)  # convert to milliseconds
        phoneme_end = int(artificial_alignment[idx][1] * 1000)  # convert to milliseconds

        if phoneme_end > len(artificial_audio):
            raise ValueError("Phoneme segment extends beyond the length of the artificial audio")

        phoneme_segment = artificial_audio[phoneme_start:phoneme_end]

        user_start_time = int(user_alignment[idx][0] * 1000)
        user_end_time = int(user_alignment[idx][1] * 1000)

        user_audio = user_audio[:user_start_time] + phoneme_segment + user_audio[user_end_time:]

        fix_wav_path = os.path.join(r'C:\Users\inbal\Desktop\SLP\backend\charsiu\src\files',
                                    'fix.wav')
        user_audio.export(fix_wav_path, format="wav")

        print("Replacement done and saved as 'fix.wav'.")

    def identify_error_v1(self, user_alignment, artificial_alignment):
        """
        this fucntion only check if need replacement on the first phoneme!
        v2 will do this to all phonemes
        """
        phoneme_classification_f_p = load_model(
    r'C:\Users\inbal\Desktop\SLP\backend\samples\pair_model\2-f-p-4000V-phonemes_22_epoches.h5')
        phoneme_classification_r_w = load_model(
            r'C:\Users\inbal\Desktop\SLP\backend\samples\pair_model\2-r-w-4000V-phonemes_22_epoches.h5')
        phoneme_classification_th_t = load_model(
            r'C:\Users\inbal\Desktop\SLP\backend\samples\pair_model\2-th-t-4000V-phonemes_22_epoches.h5')



        user_processed_wav = os.path.join(r'C:\Users\inbal\Desktop\SLP\backend\charsiu\src\files',
                                          'user_wav_processed.wav')

        user_audio_cut = ReplaceUtils.process_file(user_alignment, user_processed_wav)
        user_spectrogram = ReplaceUtils.create_spectrogram(user_audio_cut)
        predictions = self.phoneme_classification_model.predict(user_spectrogram)
        def format_predictions(predictions):
            return [f"{pred[0] * 100:.2f}% {pred[1] * 100:.2f}%" for pred in predictions]
        print(f"Predictions for user audio: {format_predictions(predictions)}")
        # todo: add here if on prediction to check if the first is not good

        return 0

#23364402
#2421892
phoneme_classification_model = load_model(
    r'C:\Users\inbal\Desktop\SLP\backend\samples\2-r-w-bigger-net.h5')

THRESHOLD = 75

phoneme_alignment_model = charsiu_forced_aligner(
    aligner='charsiu/en_w2v2_fc_10ms')
artificial_wav_path = os.path.join(r'C:\Users\inbal\Desktop\SLP\backend\charsiu\src\files',
                                   'artificial-' + 'right' + '.wav')
user_wav_path = r'C:\Users\inbal\Desktop\SLP\backend\samples\audio\white.wav'
replacer = Replacer(phoneme_alignment_model, phoneme_classification_model, "right", artificial_wav_path,
                    user_wav_path)
replacer.write_file_16k()
output_filename = os.path.join(r'C:\Users\inbal\Desktop\SLP\backend\charsiu\src\files',
                               'user_wav_processed.wav')
align = replacer.aligner(output_filename)
replacer.identify_error_v1(align,2)


