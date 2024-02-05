from pydub import AudioSegment

from pydub import AudioSegment


def inject_phoneme(first_wav_path, second_wav_path, phoneme_intervals):
    """
     This function extracts the phoneme segment from the first WAV
      file based on the specified intervals and inserts it into the second WAV 
      file at the specified insertion point.
     """
    first_wav = AudioSegment.from_file(first_wav_path, format="wav")
    second_wav = AudioSegment.from_file(second_wav_path, format="wav")

    extracted_phoneme = AudioSegment.silent(duration=0)

    for interval, _, _, _ in phoneme_intervals:
        start_time, end_time = interval
        extracted_phoneme += first_wav[start_time * 1000:end_time * 1000]

    _, _, insert_interval, _ = phoneme_intervals[0]
    insert_start, insert_end = insert_interval

    modified_second_wav = second_wav[
                          :insert_start * 1000] + extracted_phoneme + second_wav[
                                                                      insert_end * 1000:]

    return modified_second_wav


def cut_audio_by_intervals(audio_path, intervals):
    audio = AudioSegment.from_file(audio_path, format="wav")

    cut_audio = AudioSegment.silent(duration=0)

    for interval in intervals:
        start_time, end_time = interval
        cut_audio += audio[start_time * 1000:end_time * 1000]

    return cut_audio


def textGridToJson(file_path):
    with open(file_path, 'r') as file:
        textgrid_content = file.read()

    lines = textgrid_content.split('\n')

    phoneme_dict = {}

    start_index = lines.index("5") + 1

    i = start_index  # Start from the line after "5"
    while i < len(lines) and "IntervalTier" not in lines[i]:
        start_time = float(lines[i])
        end_time = float(lines[i + 1])
        phoneme = lines[i + 2].strip('"')
        phoneme_dict[(start_time, end_time)] = phoneme

        i += 3  # Move to the next set of phoneme information

    print(phoneme_dict)
    return phoneme_dict


def find_phoneme_order_differences(dict1, dict2):
    keys1 = list(dict1.keys())
    keys2 = list(dict2.keys())

    differences = []

    for key1, key2 in zip(keys1, keys2):
        if dict1[key1] != dict2[key2]:
            differences.append((key1, dict1[key1], key2, dict2[key2]))

    return differences


def runner(wrong_word: str, correct_word: str):
    file_path_wrong_word = fr'C:\Users\shirh\PycharmProjects\SLP\samples\textGrid\example_{wrong_word}.TextGrid'
    wrong_word_json = textGridToJson(file_path_wrong_word)
    file_path_correct_word = fr'C:\Users\shirh\PycharmProjects\SLP\samples\textGrid\example_{correct_word}.TextGrid'
    correct_word_json = textGridToJson(file_path_correct_word)
    phoneme_intervals = find_phoneme_order_differences(correct_word_json,
                                                       wrong_word_json)
    print(phoneme_intervals)
    first_wav_path = fr'C:\Users\shirh\PycharmProjects\SLP\samples\audio\{correct_word}.wav'
    second_wav_path = fr'C:\Users\shirh\PycharmProjects\SLP\samples\audio\{wrong_word}.wav'
    modified_second_wav = inject_phoneme(first_wav_path, second_wav_path,
                                         phoneme_intervals)

    modified_second_wav.export(
        f'../samples/results/{wrong_word}_to_{correct_word}.wav',
        format="wav")

runner("thing","sing")