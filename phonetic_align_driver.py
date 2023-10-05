from speech_recognition.wav_to_text import textIt

# sing -> sing ( sing with sing transcript )
# ([(0.0, 1.28, '[SIL]'), (1.28, 1.55, 'S'), (1.55, 1.67, 'IH'), (1.67, 1.9, 'NG'), (1.9, 2.01, '[SIL]')],
# [(0.0, 1.28, '[SIL]'), (1.28, 1.9, 'sing'), (1.9, 2.01, '[SIL]')])

# sing -> thing ( sing with thing transcript )
# ([(0.0, 1.28, '[SIL]'), (1.28, 1.53, 'TH'), (1.53, 1.67, 'IH'), (1.67, 1.9, 'NG'), (1.9, 2.01, '[SIL]')],
# [(0.0, 1.28, '[SIL]'), (1.28, 1.9, 'thing'), (1.9, 2.01, '[SIL]')])


# thing -> sing ( thing with sing transcript )
# ([(0.0, 1.08, '[SIL]'), (1.08, 1.2, 'S'), (1.2, 1.3, 'IH'), (1.3, 1.53, 'NG'), (1.53, 1.93, '[SIL]')],
# [(0.0, 1.08, '[SIL]'), (1.08, 1.53, 'sing'), (1.53, 1.93, '[SIL]')])

# thing -> thing ( thing with thing transcript )
# ([(0.0, 1.08, '[SIL]'), (1.08, 1.22, 'TH'), (1.22, 1.3, 'IH'), (1.3, 1.53, 'NG'), (1.53, 1.93, '[SIL]')],
# [(0.0, 1.08, '[SIL]'), (1.08, 1.53, 'thing'), (1.53, 1.93, '[SIL]')])

def charsiu_result(input_audio_file=None, text_to_align=None):
    return ([(0.0, 1.08, '[SIL]'), (1.08, 1.22, 'TH'), (1.22, 1.3, 'IH'), (1.3, 1.53, 'NG'), (1.53, 1.93, '[SIL]')],
            [(0.0, 1.08, '[SIL]'), (1.08, 1.53, 'thing'), (1.53, 1.93, '[SIL]')])


def extract_word_time(charsiu_result):
    target_segment = None
    for segment in charsiu_result[1]:
        if segment[2] != '[SIL]':
            target_segment = segment
    if target_segment:
        word_start_time = target_segment[0]
        word_end_time = target_segment[1]
        ph_res = []
        for ph in charsiu_result[0]:
            if ph[0] >= word_start_time and ph[1] <= word_end_time:
                ph_res.append(ph)
        return (target_segment, ph_res)
    return None






# case 1 extracted_transcript != expected_transcript
def phonetic_aligner(audio_file, expected_transcript):
    extracted_transcript = textIt(audio_file)
    print("extracted_transcript: ",extracted_transcript)

    # if extracted_transcript != expected_transcript:
    #     charsiu_result_tup = charsiu_result(audio_file,extracted_transcript)
    #     word_times = extract_word_time(charsiu_result_tup)
    #     print("wrong pronouncing of s in sing")
    #     return word_times, False

file_path = "C:\\Users\\itayy\\Desktop\\wrods\\sing.wav"
expected_transcript = "sing"
phonetic_aligner(file_path, expected_transcript)
# case 2 extracted_transcript == expected_transcript

