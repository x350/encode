import os
from chardet.universaldetector import UniversalDetector
import operator
from pprint import pprint
import json


def recognise_encoging(file):
    detector = UniversalDetector()
    with open(file, 'rb') as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        return detector.result['encoding']


def get_list_text_file(path='.'):
    list_text_file = []
    dirs = os.listdir(path)
    for item in dirs:
        if '.' in item:
            if os.path.splitext(item)[1] == '.txt':
                list_text_file.append(os.path.abspath(item))
    return list_text_file


def get_list_json_file(path='.'):
    list_json_file = []
    dirs = os.listdir(path)
    for item in dirs:
        if '.' in item:
            if os.path.splitext(item)[1] == '.json':
                list_json_file.append(os.path.abspath(item))
    return list_json_file


def get_list_xml_file(path='.'):
    list_xml_file = []
    dirs = os.listdir(path)
    for item in dirs:
        if '.' in item:
            if os.path.splitext(item)[1] == '.xml':
                list_xml_file.append(os.path.abspath(item))
    return list_xml_file


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


def count_word_in_json(file):
    all_str = ''
    word_count = {}
    encod = recognise_encoging(file)
    with open(file, 'r', encoding=encod) as f:
        data = json.load(f)
        all_str += data['rss']['channel']['title']
        all_str += data['rss']['channel']['description']
        content_item = data['rss']['channel']['items']
        for item in content_item:
            all_str += item['title']
            all_str += item['description']
    list_str = all_str.lower().split()
    for i in list_str:
        if (i in list_str) and (len(i) > 6):
            if i in word_count:
                word_count[i] += 1
            else:
                word_count[i] = 1
    word_count_tuple = word_count.items()
    word_count_result = sorted(word_count_tuple, key=operator.itemgetter(1), reverse=True)
    print(word_count_result[:10])
        


if __name__ == "__main__":
   list_text_file = get_list_text_file()
   for item in list_text_file:
       print(f"Частота слов в файле {os.path.basename(item)}:")
       count_max_occurr_word(item)

   list_json_file = get_list_json_file()
   for item in list_json_file:
       print(f"Частота слов в файле {os.path.basename(item)}:")
       count_word_in_json(item)

# count_word_in_json('newsafr.json')