import os
import soundfile as sf
import numpy as np


def convert_ogg_to_wav(folder_path):
    # List all OGG files in the directory
    files = [f for f in os.listdir(folder_path) if f.endswith('.ogg')]

    # Sort files to maintain any order if necessary (optional)
    files.sort()

    # Counter for naming new WAV files
    counter = 1

    for file in files:
        ogg_path = os.path.join(folder_path, file)

        # Read the OGG file
        data, samplerate = sf.read(ogg_path)

        # Resample if the original sample rate is not 16000 Hz
        if samplerate != 16000:
            # Number of samples in the resampled array
            number_of_samples = round(len(data) * float(16000) / samplerate)
            data = np.interp(
                np.linspace(0.0, 1.0, number_of_samples),  # Where to interpret
                np.linspace(0.0, 1.0, len(data)),  # Known positions
                data  # Known data points
            )

        # Define the new file path
        wav_path = os.path.join(folder_path, f"{counter}.wav")

        # Write the data to a WAV file with 16000 Hz sample rate
        sf.write(wav_path, data, 16000)

        # Increment the counter for the next file name
        counter += 1

        # Print the name of the newly created file
        print(f"Converted '{file}' to '{wav_path}' with sample rate 16000 Hz")


# Replace 'your_folder_path' with the path to the folder containing OGG files
convert_ogg_to_wav('C:\\Users\\inbal\\Desktop\\SLP\\backend\\samples\\w-r-wav')
