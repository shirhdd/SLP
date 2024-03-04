import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import fft
from scipy.signal import lfilter
from statsmodels.tsa.stattools import acf


def enframe(x, win, inc=None):
    """
    Splits the signal x into overlapping or non-overlapping frames with optional windowing. taken from matlab!

    Parameters:
        x (numpy array): The input signal.
        win (int or numpy array): The length of each frame or the windowing function to apply to each frame.
        inc (int, optional): The hop length between adjacent frames. Default is the length of win.

    Returns:
        f (numpy array): 2D array where each row is a frame.
        t (numpy array): Time indices for the center of each frame.
    """

    nx = len(x)
    nwin = len(win) if isinstance(win, np.ndarray) else 0

    if nwin == 0:
        len_win = win
    else:
        len_win = nwin

    if inc is None:
        inc = len_win

    nf = (nx - len_win + inc) // inc  # Number of frames
    f = np.zeros((nf, len_win))  # Initialize frames

    indf = np.arange(0, nf * inc, inc)  # Starting indices for each frame

    for i in range(nf):
        f[i, :] = x[indf[i]:indf[i] + len_win]

    if nwin > 0:  # Apply windowing function if provided
        f *= win

    t = (1 + len_win) // 2 + indf

    return f, t


def preprocess(signal, fs, alpha, window_length, overlap):
    # DC removal
    signal = signal.astype(np.float64)
    signal -= np.mean(signal)

    # Pre-emphasis filter
    b = [1, -alpha]
    a = 1
    filtered_signal = lfilter(b, a, signal)
    win_sample = int(window_length * fs)  # Number of samples for the window
    window_hamming = np.hamming(win_sample)  # Hamming window of length 'win_sample'
    inc = int(np.ceil(((win_sample + 1) * (100 - overlap)) / 100))  # Samples of overlap

    # Framing the signal
    framed_signal = enframe(filtered_signal, window_hamming, inc)

    return filtered_signal, framed_signal[0]

def FindWordIdx(FramedSig,Overlap):
    """
    Finds the indices in the original signal of the start and end of the word.
    Arguments:
    - FramedSig: the framed speech signal after preprocessing
    - Fs: sampling frequency
    - WindowLength: window length in seconds
    - Overlap: percentage of overlap between adjacent frames [0-100]
    Returns:
    - Idx: 2 integer vector, start and end indices of detected word
    """

    m, n = FramedSig.shape  # Number of windows of signal
    word_win = np.zeros(m)  # Initializing the window flag on energy

    for i in range(m):
        signal_F = fft(FramedSig[i, :])
        power_win = np.sum(signal_F * np.conj(signal_F))

        if power_win > (np.mean(np.sum(np.abs(FramedSig), axis=0)) * 4.5):
            word_win[i] = 1

    num_window_word = np.where(word_win == 1)[0]  # Finding the window number of start and end of word
    begin_win = num_window_word[0]
    end_win = num_window_word[-1]

    begin_index_first_win = ((n * Overlap) / 100) * (
                begin_win - 1) + 1  # Indices in the original signal of start and end of the word
    end_index_last_win = ((n * Overlap) / 100) * (end_win)

    Idx = [int(begin_index_first_win), int(end_index_last_win)]

    return Idx

def segmentation(signal, winlen, eta, dt, Fs, Idx):
    win_len = int(Fs * winlen)
    signal_word = signal[Idx[0]:Idx[1]]
    Overlap = (dt / winlen) * 100
    inc = int(np.ceil(((win_len + 1) * Overlap) / 100))
    sig_frames = enframe(signal_word, win_len, inc)

    m = sig_frames[0].shape[0]
    n = sig_frames[0].shape[1]

    flag = np.zeros(m)
    delta = np.zeros(len(signal_word))
    ref = sig_frames[0][0, :]
    r_0 = acf(ref, fft=True)

    spec_error_arr = []
    i = 0
    while i < m-1:
        for j in range(i + 1, m):
            test = sig_frames[0][j, :]
            r_n = acf(test, fft=True)
            spec_error = np.sum((r_n - r_0)**2) / (r_n[0] * r_0[0])
            spec_error_arr.append(spec_error)
            indx_delta = int((j - 1) * round((n * Overlap) / 100))
            delta[indx_delta:indx_delta + round((n * Overlap) / 100)] = spec_error

            if spec_error > eta:
                ref = test
                r_0 = acf(ref, fft=True)
                i = j
                flag[j] = 1
                break
        if j == m - 1:
            break

    plt.figure(figsize=(10, 4))
    plt.plot(spec_error_arr, color='b')
    plt.title('Audio Signal - shalom_example.wav spectral error')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.axhline(y=1.5, color='r', linestyle='--', label='Horizontal Line at y = 1.5')

    plt.grid()
    plt.show()

    windows_change = np.where(flag == 1)[0]
    seg_ind_temp = Idx[0] + ((n * Overlap) / 100) * (windows_change)
    seg_ind_temp2 = np.array([Idx[0]] + list(seg_ind_temp) + [Idx[1]])
    Diff_seg_len = np.diff(seg_ind_temp2)

    seg_ind_new = np.array([Idx[0]] + [0] * (len(seg_ind_temp2) - 2) + [Idx[1]])
    for i in range(1, len(seg_ind_temp2) - 1):
        if Diff_seg_len[i-1] > Fs * 0.1042:
            seg_ind_new[i] = seg_ind_temp2[i]

    seg_ind_temp3 = seg_ind_new[seg_ind_new != 0]

    #todo: change 6
    if len(seg_ind_temp3) > 6:
        seg_ind = np.concatenate((seg_ind_temp3[:5], seg_ind_temp3[-1:]))
    else:
        seg_ind = seg_ind_temp3

    return seg_ind, delta











