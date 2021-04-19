from django.core.management.base import BaseCommand
from django.conf import settings

from . import util


class Command(BaseCommand):
    help = 'Проверить промокод'

    def add_arguments(self, parser):
        parser.add_argument('-promocode', type=str, help='промокод')

    def handle(self, *args, **kwargs):
        promocode = kwargs['promocode']
        if not promocode:
            self.stdout.write('Значение \'-promocode VALUE\' обязательно.')
            return
        path = settings.PATH_JSON_FILE

        groups_data = util.get_dict_from_file(path)
        if not groups_data:
            self.stdout.write('Произошел сбой. Не удалось открыть файл. Просмотрите журнал ошибок.')
            return

        promocodes_list_dicts = list(groups_data.values())
        for group_id in range(0, len(promocodes_list_dicts)):
            if promocodes_list_dicts[group_id].get(promocode):
                group_name = list(groups_data)[group_id]
                self.stdout.write(f'Промокод \'{promocode}\' существует. группа = {group_name}')
                return
        self.stdout.write('Код не существует')
