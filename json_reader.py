"""
Разработать программу с реализацией функции для считывания json-данных из файла и вывод их в табличном виде на экран.
Реализовать базовый синтаксис для обработки исключений (try .. except)

Дополнение программы для считывания данных с использованием менеджера контекстов и реализации расширенного
синтаксиса для обработки исключений.
"""
import sys
import json

FILE_PATH = 'data.json'

BORDER = '_' * 120


def load_json(file_path=FILE_PATH, to_print=False, test_mode=False):
    data = []
    try:
        with open(file_path, 'rt') as f:
            json_txt = f.read()
        try:
            data = json.loads(json_txt)
        except json.decoder.JSONDecodeError:
            if to_print:
                print(f'File contains syntax errors')
    except FileNotFoundError:
        if to_print:
            print(f'File not found at {FILE_PATH}')

    finally:
        # Headers
        if to_print:
            if len(data) > 0:
                headers = data[0].keys()
                header = ' | '.join(headers)
            # Data
            for person in data:
                print(BORDER)
                tr = ' | '.join((str(val) for val in person.values()))
                print(tr)
    return data


if __name__ == '__main__':
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        load_json(to_print=True, test_mode=True)
