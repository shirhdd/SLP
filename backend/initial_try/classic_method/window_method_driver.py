import numpy as np
from matplotlib import pyplot as plt
from scipy.io import wavfile

from backend.initial_try.classic_method.const import SUCCESS_PHONEME_RECOGNITION_EXAMPLE_WAV_FILE_PATH, WINDOW_LENGTH, OVERLAP, ETA, DT
from backend.initial_try.classic_method.window_method_utils import preprocess, FindWordIdx, segmentation

# PART 1: PLOT THE SIGNAL
alpha = 0.99
b = [1 - alpha];
a = 1;
shalom_Fs, shalom = wavfile.read(SUCCESS_PHONEME_RECOGNITION_EXAMPLE_WAV_FILE_PATH)
# shalom_Fs, shalom = wavfile.read('C:\\Users\\itayy\\Desktop\\engineering_projects\\Itay-voice.wav')

duration = len(shalom) / shalom_Fs

# Create a time vector
time = np.linspace(0, duration, len(shalom))
# normalization
shalom = shalom / max(shalom)
# Plot the audio signal
plt.figure(figsize=(10, 4))
plt.plot(time, shalom, color='b')
plt.title('Audio Signal - shalom_example.wav')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid()
plt.show()
# PART 2: PLOT THE PROCESSED SIGNAL
ProcessedSig, FramedSig = preprocess(shalom, shalom_Fs, alpha, WINDOW_LENGTH, OVERLAP);
Idx = FindWordIdx(FramedSig, OVERLAP)
# print(Idx)
plt.figure(figsize=(10, 4))
plt.plot(time, ProcessedSig, color='b')
plt.title('Audio Signal - shalom_example.wav after preprocess')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.axvline(x=time[Idx[0]], color='r', linestyle='--', label='Start of Word')
plt.axvline(x=time[Idx[1]], color='r', linestyle='--', label='End of Word')

# Adding a legend to the plot
plt.legend()
plt.grid()
plt.show()

# PART 3: PLOT SIGNAL WITH PHONEMES SEGMENTATION
T = 1 / shalom_Fs
N = len(shalom)
t = np.arange(0, T * (N - 1) + T, T)  # Create time vector

signal = ProcessedSig
Fs = shalom_Fs

seg_ind1, delta1 = segmentation(signal, WINDOW_LENGTH, ETA, DT, Fs, Idx)
seg_ind1 = [0] + seg_ind1

plt.figure(figsize=(10, 4))
# Initialize a color index to cycle through colors
color_index = 0

for i in range(len(seg_ind1) - 1):
    start = seg_ind1[i]
    end = seg_ind1[i + 1]
    color = ['b', 'g', 'c', 'm', 'y'][color_index]  # Choose a color for this segment
    plt.plot(time[start:end], shalom[start:end], color=color, label=f'Segment {i + 1}')

    # Update color index
    color_index = (color_index + 1) % 5

# Add the last segment
plt.plot(time[seg_ind1[-1]:], shalom[seg_ind1[-1]:], color=['b', 'g', 'c', 'm', 'y'][color_index],
         label=f'Segment {len(seg_ind1)}')

plt.title('Audio Signal - shalom_example.wav after add seg')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
for seg in seg_ind1:
    plt.axvline(x=time[seg], color='r', linestyle='--', label='Start of Word')

plt.grid()
plt.show()

# todo: add here the formants from matlab
