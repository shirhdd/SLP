# import essential libraries
import os
import sys

# change this path to where you saved the charsiu package
charsiu_dir = 'C:\\Users\\shirh\\PycharmProjects\\SLP\\charsiu\\'
os.chdir(charsiu_dir)

sys.path.append('%s/src/' % charsiu_dir)

# import selected model from Charsiu
from Charsiu import charsiu_predictive_aligner

# initialize model
charsiu = charsiu_predictive_aligner(aligner='charsiu/en_w2v2_fc_10ms')

# load data
audio_file = 'C:\\Users\\shirh\\PycharmProjects\\SLP\\sample_audio\\sing.wav'
textgrid_file = r'C:\Users\shirh\PycharmProjects\SLP\exmple_sing.TextGrid'
txt_file = r'/samples/text/sing.txt'

# import selected model from Charsiu
from Charsiu import charsiu_forced_aligner

# initialize model
charsiu = charsiu_forced_aligner(aligner='charsiu/en_w2v2_fc_10ms')

# read in text file
with open(txt_file) as f:
    text = f.read()

# perform forced alignment
alignment = charsiu.align(audio=audio_file,text=text)

# perform forced alignment and save the output as a textgrid file
charsiu.serve(audio=audio_file, text=text,
              save_to=textgrid_file)
