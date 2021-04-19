import os
import random
from faker import Faker

from django.core.management.base import BaseCommand
from django.conf import settings

from . import util

fake = Faker()
Faker.seed(5)


def generate_base_file():
    groups_dict = {}
    for _ in range(0, 3): groups_dict.update({fake.color_name(): {}})

    for _ in range(0, 58):
        groups_dict.get(random.choice(list(groups_dict.keys()))).update(
            {fake.word(): fake.random_int(min=1, max=50)})
    return groups_dict


class Command(BaseCommand):
    help = 'Создать файл с промокодами'

    def add_arguments(self, parser):
        parser.add_argument('-g', type=int, help='Количество групп')
        parser.add_argument('-p', type=int, help='Количество промокодов', )

    def handle(self, *args, **kwargs):
        count_groups = kwargs['g'] or 3
        count_promocodes = kwargs['p'] or 58
        path = settings.PATH_JSON_FILE
        groups_dict = {}

        for _ in range(0, count_groups): groups_dict.update({fake.color_name(): {}})

        for _ in range(0, count_promocodes):
            groups_dict.get(random.choice(list(groups_dict.keys()))).update(
                {fake.word(): fake.random_int(min=1, max=50)}
            )
        """
        Знаю, что 2 идентичных util в одном проекте быть не должны. Но Подключать util из приложения, на мой взгляд
        было некорректно. Подключать к API код из этого util, сомневаюсь. Поэтому оставил в таком костыльном виде. :)
        """
        util.write_dict_in_file(path, groups_dict)
        if os.path.exists(path): text = 'Файл успешно создан.'
        else: text = 'Произошел сбой. Не удалось создать файл. Просмотрите журнал ошибок.'
        self.stdout.write(text)
