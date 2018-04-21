import os
from chardet.universaldetector import UniversalDetector
import operator
import json
import xml.etree.ElementTree as ET


def recognise_encoging(file):
    detector = UniversalDetector()
    with open(file, 'rb') as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                break
    detector.close()
    return detector.result['encoding']


def get_list_file(path='.', extend='.txt'):
    list_file = []
    dirs = os.listdir(path)
    for item in dirs:
        if '.' in item:
            if os.path.splitext(item)[1] == extend:
                list_file.append(os.path.abspath(item))
    return list_file


def text_file_to_list_word(file):
    encod = recognise_encoging(file)
    with open(file, 'r', encoding=encod) as f:
        return f.read().lower().split()


def json_file_to_list_word(file):
    all_str = ''
    encod = recognise_encoging(file)
    with open(file, 'r', encoding=encod) as f:
        data = json.load(f)
        all_str += data['rss']['channel']['title']
        all_str += data['rss']['channel']['description']
        content_item = data['rss']['channel']['items']
        for item in content_item:
            all_str += item['title']
            all_str += item['description']
    return all_str.lower().split()


def xml_file_to_list_word(file):
    all_str = ''
    encod = recognise_encoging(file)
    xmlparser = ET.XMLParser(encoding=encod)
    tree = ET.parse(file, parser=xmlparser)
    for elem in tree.getiterator():
        if elem.tag == 'title':
            all_str += elem.text
        elif elem.tag == 'description':
            all_str += elem.text
    return all_str.lower().split()


def count_word(list_word):
    word_count = {}
    for i in list_word:
        if (i in list_word) and (len(i) > 6):
            if i in word_count:
                word_count[i] += 1
            else:
                word_count[i] = 1
    word_count_tuple = word_count.items()
    word_count_result = sorted(word_count_tuple, key=operator.itemgetter(1), reverse=True)
    print(word_count_result[:10])


if __name__ == "__main__":
    for item in get_list_file():
        print(f"Частота слов в файле {os.path.basename(item)}:")
        count_word(text_file_to_list_word(item))

    for item in get_list_file(extend='.json'):
        print(f"Частота слов в файле {os.path.basename(item)}:")
        count_word(json_file_to_list_word(item))

    for item in get_list_file(extend='.xml'):
        print(f"Частота слов в файле {os.path.basename(item)}:")
        count_word(xml_file_to_list_word(item))
