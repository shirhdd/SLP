import os
import sys
from scipy.io import wavfile
from scipy.signal import resample

# change this path to where you saved the charsiu package
ENV = r'C:\Users\shirh\PycharmProjects\SLP'
charsiu_dir = fr'{ENV}\\charsiu\\'
os.chdir(charsiu_dir)
sys.path.append('%s\src\\' % charsiu_dir)
from Charsiu import charsiu_predictive_aligner
from Charsiu import charsiu_forced_aligner


def textless_alignment(audio_file, textgrid_file):
    # initialize model
    charsiu = charsiu_predictive_aligner(aligner='charsiu/en_w2v2_fc_10ms')
    # perform textless alignment
    alignment = charsiu.align(audio=audio_file)
    ## print (start_time, end_time, 'segment_label')
    print(alignment)

    # OR, you can perform textless alignment and output the results directly to a textgrid file
    charsiu.serve(audio=audio_file, save_to=textgrid_file)


def resample_wav(input_file, target_fs):
    # Read the input wav file
    fs, data = wavfile.read(input_file)

    # Resample the data
    resampled_data = resample(data, int(len(data) * target_fs / fs))

    # Write the resampled data to a new wav file
    wavfile.write(input_file, target_fs, resampled_data.astype(data.dtype))


def forced_alignment(audio_file, textgrid_file, txt_file):
    charsiu = charsiu_forced_aligner(aligner='charsiu/en_w2v2_fc_10ms')
    with open(txt_file) as f:
        text = f.read()
    alignment = charsiu.align(audio=audio_file, text=text)
    charsiu.serve(audio=audio_file, text=text,
                  save_to=textgrid_file)


def main():
    # load data
    audio_file = fr'{ENV}\samples\audio\white.wav'
    textgrid_file = fr'{ENV}\samples\textGrid\example_white.TextGrid'
    txt_file = fr'{ENV}\samples\text\white.txt'
    resample_wav(audio_file, 16000)
    forced_alignment(audio_file, textgrid_file, txt_file)


if __name__ == '__main__':
    main()
