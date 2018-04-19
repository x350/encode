import os
from chardet.universaldetector import UniversalDetector
import operator


def recognise_encoging(file):
    detector = UniversalDetector()
    with open(file, 'rb') as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        return detector.result['encoding']
# print(recognise_encoging('newsafr.txt'))


# def get_list_text_file(path='.'):
#     list_text_file = []
#     dirs = os.listdir(path)
#     for item in dirs:
#         if '.' in item:
#             if item.split('.')[1] == 'txt': # для других расширений попробывать- отдельный if.
#                 list_text_file.append(os.path.abspath(item))
#     return list_text_file


def get_list_text_file(path='.'):
    list_text_file = []
    dirs = os.listdir(path)
    for item in dirs:
        if '.' in item:
            if os.path.splitext(item)[1] == '.txt': # для других расширений попробывать- отдельный if.
                list_text_file.append(os.path.abspath(item))
    return list_text_file


def count_max_occurr_word(file):
    word_count = {}
    encod = recognise_encoging(file)
    with open(file, 'r', encoding=encod) as f:
        data = f.read().lower().split()
        for i in data:
            if (i in data) and (len(i) > 6):
                if i in word_count:
                    word_count[i] += 1
                else:
                    word_count[i] = 1
    word_count_tuple = word_count.items()
    word_count_result = sorted(word_count_tuple, key=operator.itemgetter(1), reverse=True)
    print(word_count_result[:10])


list_text_file = get_list_text_file()
for item in list_text_file:
    print(f"Частота слов в файле {os.path.basename(item)}:")
    count_max_occurr_word(item)