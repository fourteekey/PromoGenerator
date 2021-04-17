import logging
import secrets
import json

logger = logging.getLogger(__name__)


def check_promo(list_values):
    promocode = secrets.token_urlsafe(3)
    for data in list_values:
        if promocode in data.keys():
            check_promo(list_values)
            break
    return promocode


def get_dict_from_file(PATH):
    """ Прочитать данные с файла и вернуть словарь."""
    try:
        with open(PATH) as json_file: json_list_str = json_file.readlines()
    except Exception as e:
        logger.error(f'Cannot read file. | {e}')
        return None

    json_file.close()
    # Преобразовуем строки в словарь для проверки на наличие промокода
    res_str = ''
    for _ in json_list_str: res_str += _
    # Удаляем запятую вконце строки
    return json.loads('{' + res_str[:-2] + '}')


def write_dict_in_file(PATH, res_dict, new_line=None):
    """ Записать новые промокоды в файл."""
    if new_line: mode = 'a'
    else: mode = 'w'

    try:
        with open(PATH, mode) as json_file:
            for _ in res_dict.keys():
                # Записываем данные в файл. Разбиваем группы построчно
                text = '\"' + str(_) + '\": ' + json.dumps(res_dict[_]) + ',\n'
                json_file.write(text)

    except Exception as e:
        logger.error(f'Cannot open and write in file | {e}')
        return

    return 1
