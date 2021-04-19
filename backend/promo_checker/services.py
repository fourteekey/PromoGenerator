import random

from . import util


def generate_base_file(path):
    # Знаю что не по PEP, но запрос нужен на 1 раз.
    from faker import Faker

    fake = Faker()
    Faker.seed(5)

    groups_dict = {}
    for _ in range(0, 3): groups_dict.update({fake.color_name(): {}})

    for _ in range(0, 58):
        groups_dict.get(random.choice(list(groups_dict.keys()))).update({fake.word(): fake.random_int(min=1, max=50)})
    return util.write_dict_in_file(path, groups_dict)


def get_promocode(promocode, path):
    groups_data = util.get_dict_from_file(path)
    # Если не удалось открыть файл
    if not groups_data: return

    promocodes_list_dicts = list(groups_data.values())
    for group_id in range(0, len(promocodes_list_dicts)):
        if promocodes_list_dicts[group_id].get(promocode):
            group_name = list(groups_data)[group_id]
            return {'group_name': group_name, 'promocode': promocode, 'value': groups_data[group_name][promocode]}
    return


def insert_new_promo(group_name, amount: int, path):
    groups_data = util.get_dict_from_file(path)
    if not groups_data: return

    promocodes_list = list(groups_data.values())

    promocode = util.check_promo(promocodes_list)
    if group_name in groups_data.keys(): groups_data[group_name].update({str(promocode): amount})
    else: groups_data.update({group_name: {promocode: amount}})

    write_flag = util.write_dict_in_file(path=path, groups_data=groups_data)
    if write_flag: return promocode
