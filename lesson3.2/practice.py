import requests
import os.path
from chardet.universaldetector import UniversalDetector


def translate_it(lang, text):
    """
    YANDEX translation plugin
    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    :param text: <str> text for translation.
    :return: <str> translated text.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'

    params = {
        'key': key,
        'lang': lang,
        'text': text,
    }
    response = requests.get(url, params=params).json()
    return ' '.join(response.get('text', []))


def recognise_encoding(file):
    detector = UniversalDetector()
    with open(file, 'rb') as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                break
    detector.close()
    return detector.result['encoding']


def take_input_path():
    input_path = input('Введите путь к файлу (с именем файла): ')
    if not os.path.exists(input_path):
        print('Файл не найден')
        exit(1)
    return input_path


def get_result_path():
    output_path = input('Введите путь к файлу с результатом (с именем файла): ')
    temp_path = os.path.dirname(output_path)
    if temp_path != '':
        if not os.path.exists(temp_path):
            print('Указанного пути не существует')
            exit(2)
    return output_path


def input_lang():
    return input('Введите язык, с которого перевести: ')


def output_lang():
    return input('Введите язык, на который перевести: ')


def load_text(path):
    with open(path, 'r', encoding=recognise_encoding(path)) as f:
        return f.read()


def write_text(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


if __name__ == '__main__':
    a = translate_it('-'.join((input_lang(), output_lang())), load_text(take_input_path()))
    write_text(get_result_path(), a)
    print(a)
