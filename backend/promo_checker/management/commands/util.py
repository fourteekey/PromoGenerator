import logging
import secrets
import json

logger = logging.getLogger(__name__)


def check_promo(promocodes_list):
    promocode = secrets.token_urlsafe(3)
    for data in promocodes_list:
        if promocode in data.keys():
            check_promo(promocodes_list)
            break
    return promocode


def get_dict_from_file(path):
    """ Прочитать данные с файла и вернуть словарь."""
    try:
        with open(path) as json_file: json_data = json.load(json_file)
    except Exception as e:
        logger.error(f'Cannot read file. | {e}')
        return None

    json_file.close()
    return json_data


def write_dict_in_file(path, groups_data):
    """ Записать новые промокоды в файл."""
    try:
        with open(path, 'w') as json_file: json.dump(groups_data, json_file)
    except Exception as e:
        logger.error(f'Cannot open and write in file | {e}')
        return

    return 1
