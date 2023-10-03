import librosa
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import spectrogram
# from python_speech_features import mfcc


def spectrogram_creation(y, sr, index=None, times=None):
    """
    Compute and plot the spectrogram of the given audio signal with annotated time intervals.

    Parameters:
    - y: array-like
        Audio signal.
    - sr: int
        Sampling rate of the audio signal.
    - index: tuple of int, optional
        Starting and ending indices to slice the audio signal. If provided, only this segment will be used.
    - times: list of tuples, optional
        List of time intervals (start_time, end_time, name) to annotate on the plot.
    """
    if index:
        y = y[index[0]:index[1]]
    nperseg = int(sr * 0.025)  # Window length of 0.025 seconds
    noverlap = nperseg - int(sr * 0.01)  # Steps of 0.01 seconds

    # Calculate the spectrogram with Hamming window
    frequencies, time_samples, Sxx = spectrogram(y, sr, window=np.hamming(nperseg), nperseg=nperseg, noverlap=noverlap)

    # Convert provided time intervals to sample indices
    if times:
        time_indices = [(int(start_time * sr), int(end_time * sr), name) for start_time, end_time, name in times]

    # Plot the spectrogram
    plt.pcolormesh(time_samples, frequencies, 10 * np.log10(Sxx), shading='gouraud')
    plt.colorbar(label='Intensity [dB]')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.title('Spectrogram with Hamming Window')

    # Annotate time intervals on the plot
    if times:
        for start_idx, end_idx, name in time_indices:
            plt.axvline(x=start_idx / sr, color='r', linestyle='--', label=name)
            plt.axvline(x=end_idx / sr, color='r', linestyle='--')

    plt.legend(loc='upper right')
    plt.show()

    return time_samples, frequencies, 10 * np.log10(Sxx)


# def mfcc_spectrogram_creation(y, sr, index=None):
#     """
#     Compute and plot the MFCC spectrogram of the given audio signal.
#
#     Parameters:
#     - y: array-like
#         Audio signal.
#     - sr: int
#         Sampling rate of the audio signal.
#     - index: tuple of int, optional
#         Starting and ending indices to slice the audio signal. If provided, only this segment will be used.
#     """
#     if index:
#         y = y[index[0]:index[1]]
#     mfcc_features = mfcc(y, samplerate=sr, winlen=0.025, winstep=0.01, numcep=13, nfilt=26, nfft=512, lowfreq=0,
#                          highfreq=None, preemph=0.97, winfunc=np.hamming)
#
#     # # Plot the MFCCs
#     # # Transpose for the visualization to make time on x-axis
#     # mfcc_features = mfcc_features.T
#     # fig, ax = plt.subplots(figsize=(10, 4))
#     # cax = ax.imshow(mfcc_features, aspect='auto', cmap='inferno', origin='lower')
#     # fig.colorbar(cax, label='Intensity')
#     # ax.set_ylabel('MFCC Coefficients')
#     # ax.set_xlabel('Time Frame')
#     # ax.set_title('MFCC Spectrogram sh1')
#     # plt.tight_layout()
#     # plt.show()
#     return mfcc_features


# y, sr = librosa.load('C:\\Users\\itayy\\Desktop\\engineering_projects\\shalom_example.wav', sr=16000)
# spectrogram_creation(y, sr, index=None)
# s = mfcc_spectrogram_creation(y, sr,
#                               index=None)
