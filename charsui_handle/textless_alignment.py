# import essential libraries
import os
import sys

# change this path to where you saved the charsiu package
charsiu_dir = 'C:\\Users\\shirh\\PycharmProjects\\SLP\\charsiu\\'
os.chdir(charsiu_dir)

sys.path.append('%s\src\\' % charsiu_dir)

# import selected model from Charsiu
from Charsiu import charsiu_predictive_aligner

# initialize model
charsiu = charsiu_predictive_aligner(aligner='charsiu/en_w2v2_fc_10ms')

# load data
## Here are some example paths. Remember to replace with your own paths.
audio_file = 'C:\\Users\\shirh\\PycharmProjects\\SLP\\sample_audio\\sing.wav'
textgrid_file = r'C:\Users\shirh\PycharmProjects\SLP\exmple_sing.TextGrid'

# perform textless alignment
## replace the audio path with the path for your own audio file.
alignment = charsiu.align(audio=audio_file)
## print (start_time, end_time, 'segment_label')
print(alignment)

# OR, you can perform textless alignment and output the results directly to a textgrid file
charsiu.serve(audio=audio_file, save_to=textgrid_file)