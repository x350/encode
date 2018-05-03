# -*- coding: utf-8 -*-
import os
from chardet.universaldetector import UniversalDetector


def recognise_encoging(file):
    detector = UniversalDetector()
    with open(file, 'rb') as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                break
    detector.close()
    return detector.result['encoding']


def get_list_file(dir_file, extend='.sql'):
    list_file = []
    files_in_dir = os.listdir(os.path.join(current_dir, dir_file))
    for item in files_in_dir:
        if os.path.splitext(item)[1] == extend:
            list_file.append(os.path.join(current_dir, dir_file, item))
    return list_file


def input_substring():
    return input('Input substring: ')


def found_substring_in_file(file, substring):
    with open(file, 'r', encoding=recognise_encoging(file)) as f:
        for line in f:
            if substring in line:
                return os.path.abspath(file)


def check_list(list_file, my_substring):
    result_list = []
    for item in list_file:
        i = found_substring_in_file(item, my_substring)
        if i:
            result_list.append(i)
            print(i)
    print(f'Total: {len(result_list)}')
    return result_list

if __name__ == '__main__':
    dir_with_files = 'Migrations'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    list_found_file = get_list_file(dir_file=dir_with_files)
    while True:
        user_request = input_substring()
        if user_request == 'q':
            break
        list_found_file = check_list(list_found_file, user_request)
        if len(list_found_file) <= 1:
            break
