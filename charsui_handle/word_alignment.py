import os
import sys

# change this path to where you saved the charsiu package
charsiu_dir = r'C:\Users\\shirh\\PycharmProjects\\SLP\\charsiu\\'
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


def forced_alignment(audio_file, textgrid_file, txt_file):
    charsiu = charsiu_forced_aligner(aligner='charsiu/en_w2v2_fc_10ms')
    with open(txt_file) as f:
        text = f.read()
    alignment = charsiu.align(audio=audio_file, text=text)
    charsiu.serve(audio=audio_file, text=text,
                  save_to=textgrid_file)


def main():
    # load data
    audio_file = r'C:\Users\shirh\PycharmProjects\SLP\samples\audio\thing.wav'
    textgrid_file = r'C:\Users\shirh\PycharmProjects\SLP\samples\textGrid\example_thing.TextGrid'
    txt_file = r'C:\Users\shirh\PycharmProjects\SLP\samples\text\thing.txt'

    forced_alignment(audio_file, textgrid_file, txt_file)


if __name__ == '__main__':
    main()
