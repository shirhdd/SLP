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


def find_phoneme_order_differences(dict1, dict2):
    keys1 = list(dict1.keys())
    keys2 = list(dict2.keys())

    differences = []

    # Check differences based on the order of phonemes
    for key1, key2 in zip(keys1, keys2):
        if dict1[key1] != dict2[key2]:
            differences.append((key1, dict1[key1], dict2[key2]))

    return differences


file_path = r'C:\Users\shirh\PycharmProjects\SLP\samples\textGrid\exmple_sing.TextGrid'
textGridToJson(file_path)
