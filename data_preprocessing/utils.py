import librosa
import soundfile as sf

def resample_and_save_audio(input_path, output_path, target_sample_rate=16000):
    try:
        # Load the audio file using librosa
        audio, sr = librosa.load(input_path, sr=None)

        # Resample the audio to the target sample rate
        resampled_audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sample_rate)

        # Save the resampled audio to the specified output path with the same name
        sf.write(output_path, resampled_audio, target_sample_rate)
        print(f"Audio resampled and saved to {output_path} with a sample rate of {target_sample_rate} Hz.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_sample_rate(wav_file_path):
    try:
        # Load the audio file using librosa
        audio, sample_rate = librosa.load(wav_file_path, sr=None)
        print(sample_rate)
        return sample_rate
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def silence_samples(y , start_sample, end_sample):
    if start_sample < 0:
        start_sample = 0
    if end_sample > len(y):
        end_sample = len(y)

    y[start_sample:end_sample] = 0
    return y

