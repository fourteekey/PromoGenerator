import random

from . import util


def generate_base_file(PATH):
    # Знаю что не по PEP, но запрос нужен на 1 раз.
    from faker import Faker

    fake = Faker()
    Faker.seed(5)

    res_dict = {}
    for _ in range(0, 3): res_dict.update({fake.color_name(): {}})

    for _ in range(0, 58):
        res_dict.get(random.choice(list(res_dict.keys()))).update({fake.word(): fake.random_int(min=1, max=50)})
    return util.write_dict_in_file(PATH, res_dict)


def get_promocode(promocode, PATH):
    mydict = util.get_dict_from_file(PATH)
    # На случай, если не удалось открыть файл
    if not mydict: return

    # Получаем список ключей всех груп в формате [{data_1_group_1: key}, {data_2_group_2: key}]
    list_values = list(mydict.values())
    for _ in range(0, len(list_values)):
        # Если нашли нужный промокод приостанавливаем итерацию. и сохраняем индекс группы
        if list_values[_].get(promocode):
            # Получаем группу по индексу
            group_name = list(mydict)[_]
            # Значение берем классически из словаря
            return {'group_name': group_name, 'promocode': promocode, 'value': mydict[group_name][promocode]}

    return


def insert_new_promo(group_name, amount: int, PATH):
    mydict = util.get_dict_from_file(PATH)
    if not mydict: return

    list_values = list(mydict.values())

    # Рекурсивная функция на проверку оригинальности промокода.
    promocode = util.check_promo(list_values)
    if group_name in mydict.keys():
        # Изменяем предыдущий словарь
        mydict[group_name].update({str(promocode): amount})
        res = util.write_dict_in_file(PATH=PATH, res_dict=mydict)
    else:
        mydict = {group_name: {promocode: amount}}
        res = util.write_dict_in_file(PATH=PATH, res_dict=mydict, new_line=1)
    # Отправляем ЗАПИСАННЫЙ В ФАЙЛ промокод.
    if res: return promocode
