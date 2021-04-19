from django.core.management.base import BaseCommand
from django.conf import settings

from . import util


class Command(BaseCommand):
    help = 'Добавить промокод в файл.'

    def add_arguments(self, parser):
        parser.add_argument('-group', type=str, help='Название группы', )
        parser.add_argument('-amount', type=int, help='Значение промокода.')

    def handle(self, *args, **kwargs):
        group_name = kwargs['group']
        amount = kwargs['amount']
        if not group_name or not amount:
            self.stdout.write('Отсуствуют обязательные аргументы. '
                              'Пример команды python manage.py -group FirstGroup -amount 5')
            return
        elif amount == 0:
            self.stdout.write('Значение \'-amount\' не может быть нулем.')
            return

        path = settings.PATH_JSON_FILE

        groups_data = util.get_dict_from_file(path)
        if not groups_data:
            self.stdout.write('Произошел сбой. Не удалось открыть файл. Просмотрите журнал ошибок.')
            return

        promocodes_list = list(groups_data.values())

        promocode = util.check_promo(promocodes_list)
        if group_name in groups_data.keys():
            groups_data[group_name].update({promocode: amount})
        else:
            groups_data.update({group_name: {promocode: amount}})

        write_flag = util.write_dict_in_file(path=path, groups_data=groups_data)
        if write_flag:
            text = f'Значение добавлено в группу: \'{group_name}\'. Промокод: {promocode}'
        else:
            text = 'Произошел сбой. Не удалось добавить значение.'
        self.stdout.write(text)
