import os

import numpy as np
from matplotlib import pyplot as plt


def count_wav_files(root_directory):
    """Count all .wav files by their names in the folder structure."""

    wav_files = {}

    # Walk through the root directory
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for file in filenames:
            if file.endswith('.wav'):
                # Increment the count for this file name, or set it to 1 if it's the first occurrence
                wav_files[file] = wav_files.get(file, 0) + 1

    return wav_files


def plot_counts(count_dict):
    """Plot a bar graph of file counts with statistics, excluding sa1.wav and sa2.wav."""

    sa1_count = count_dict.pop('sa1.wav', 0)
    sa2_count = count_dict.pop('sa2.wav', 0)

    file_names = list(count_dict.keys())
    counts = list(count_dict.values())

    # Calculate statistics
    mean_count = np.mean(counts)
    max_count = np.max(counts)
    min_count = np.min(counts)
    std_count = np.std(counts)

    plt.figure(figsize=(12, 6))
    plt.bar(file_names, counts, color='blue')

    # Display statistics on the graph
    plt.axhline(mean_count, color='red', linestyle='dashed', linewidth=1)
    plt.text(0, mean_count + 0.5, f'Mean: {mean_count:.2f}', color='red')
    plt.axhline(max_count, color='green', linestyle='dashed', linewidth=1)
    plt.text(0, max_count + 0.5, f'Max: {max_count}', color='green')
    plt.axhline(min_count, color='yellow', linestyle='dashed', linewidth=1)
    plt.text(0, min_count + 0.5, f'Min: {min_count}', color='yellow')
    plt.axhline(mean_count - std_count, color='purple', linestyle='dashed', linewidth=1)
    plt.axhline(mean_count + std_count, color='purple', linestyle='dashed', linewidth=1)
    plt.text(0, mean_count + std_count + 0.5, f'Std: +/- {std_count:.2f}', color='purple')

    # Note for excluded files
    plt.annotate(f"* Excluded: sa1.wav ({sa1_count} times), sa2.wav ({sa2_count} times)",
                 xy=(1, 1.02), xycoords='axes fraction', fontsize=10, ha='right')

    plt.xlabel('File Names')
    plt.ylabel('Counts')
    plt.title('Count of .wav Files by Name with Statistics')
    plt.xticks(rotation=45, ha="right")  # Rotate file names for better visibility
    plt.tight_layout()
    plt.show()

root_directory ='C:\\Users\\itayy\\Desktop\\engineering_projects\\timit\\train'
wav_file_counts = count_wav_files(root_directory)

# Plot the results
plot_counts(wav_file_counts)
