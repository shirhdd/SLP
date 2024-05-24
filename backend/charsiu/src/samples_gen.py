# import sys
#
# import scipy
# import soundfile as sf
# import tensorflow as tf
# from scipy.io import wavfile
#
# import soundfile as sf
# import scipy.io.wavfile as wavfile
# import os
#
# from backend.charsiu.src.Charsiu import charsiu_forced_aligner
#
#
# def read_transcript_to_array(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
#     return [line.strip() for line in lines]  # Remove any trailing newline characters
#
#
# def write_file_16k(file_path, output_path, segment_start=None, segment_end=None, segment_output_path=None):
#     # Load the audio file
#     audio, sample_rate = sf.read(file_path)
#
#     # Ensure the sample rate is 16 kHz
#     assert sample_rate == 16000, "The sample rate of the audio file is not 16 kHz"
#
#     # Convert to int16 format
#     audio_int16 = (audio * 32767).astype('int16')
#
#     # Ensure the output directory exists
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)
#
#     # Write the full audio to a new WAV file
#     wavfile.write(output_path, sample_rate, audio_int16)
#
#     if segment_start is not None and segment_end is not None:
#         # Calculate the sample indices for the segment
#         start_sample = int(segment_start * sample_rate)
#         end_sample = int(segment_end * sample_rate)
#
#         # Extract the segment
#         audio_segment = audio_int16[start_sample:end_sample]
#
#         # Ensure the output directory for the segment exists
#         os.makedirs(os.path.dirname(segment_output_path), exist_ok=True)
#
#         # Write the segment to a new WAV file
#         wavfile.write(segment_output_path, sample_rate, audio_segment)
#
#
# # Specify the path to the FLAC audio file
# file_path_audio = r'C:\Users\inbal\Desktop\SLP\backend\LIBRISPEECH\LibriSpeech\dev-clean\174\50561\174-50561-0000.flac'
#
# # Specify the output path for the new WAV file
# output_path_wav = r'C:\Users\inbal\Desktop\SLP\backend\charsiu\src\processed_16k.wav'
# segment_output_path_wav = r'C:\Users\inbal\Desktop\SLP\backend\charsiu\src\one_word.wav'
#
# # Call the function to process and save the audio file
# write_file_16k(file_path_audio, output_path_wav, segment_start=2.61, segment_end=2.94, segment_output_path=segment_output_path_wav)
#
# file_path_transcript = r'C:\Users\inbal\Desktop\SLP\backend\LIBRISPEECH\LibriSpeech\dev-clean\174\50561\174-50561.trans.txt'
#
# # Read the contents of the transcript file into an array
# transcript_lines = read_transcript_to_array(file_path_transcript)
# transcript_lines = " ".join(transcript_lines[0].split(" ")[1:])
# # print(transcript_lines)
# # phoneme_alignment_model = charsiu_forced_aligner(
# #     aligner='charsiu/en_w2v2_fc_10ms')
# #
# # alignment = phoneme_alignment_model.align(audio='processed_16k.wav',
# #                                           text=transcript_lines)
# #
# # print(transcript_lines)
# # print(alignment)
# # text = "FORGOTTEN TOO THE NAME OF GILLIAN THE LOVELY CAPTIVE"
# print(sys.executable)

import os
from pydub import AudioSegment

def convert_ogg_to_wav(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".ogg"):
            # Construct the full path to the .ogg file
            ogg_file_path = os.path.join(folder_path, filename)
            # Load the .ogg file
            audio = AudioSegment.from_ogg(ogg_file_path)
            # Set the sample rate to 16000
            audio = audio.set_frame_rate(16000)
            # Construct the new file name with .wav extension
            wav_file_path = os.path.join(folder_path, os.path.splitext(filename)[0] + ".wav")
            # Export the audio as a .wav file
            audio.export(wav_file_path, format="wav")
            print(f"Converted {filename} to {os.path.basename(wav_file_path)}")

# Example usage
folder_path = "C:\\Users\\inbal\\Desktop\\SLP\\backend\\samples\\s-sh-wav"
convert_ogg_to_wav(folder_path)

