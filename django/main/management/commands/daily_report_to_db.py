import os
from loguru import logger
from datetime import datetime
from main.models import Warehouse, Username, Organizer, Transaction, ReductionFine
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Очистка данных из скачанного отчёта и вставка их в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('warh')
        parser.add_argument('filename')

    @logger.catch
    def handle(self, *args, **options):
        with open(f'./reports/xls/{options["warh"]}/daily/{options["filename"]}', 'r') as f:
            soup = BeautifulSoup (f, 'html.parser')
            rows = soup.find_all('tr')

            clear_data = []
            decreases = {}
            prolongation = {}

            for i, row in enumerate(rows):
                raw_line = row.find_all('td')
                clear_line = []
                for line in raw_line:
                    if line.get('colspan'):
                        if line.get('colspan') == '1':
                            decreases[rows[i-1].find_all('td')[0].string] = int(line.string.replace('- ', '').strip())
                        elif line.get('colspan') == '5':
                            if rows[i-1].find_all('td')[0].string.strip() ==  "В том числе с уменьшением штрафа":
                                prolongation[rows[i-2].find_all('td')[0].string] = line.string.strip()
                            else:
                                prolongation[rows[i-1].find_all('td')[0].string] = line.string.strip()
                    else:
                        clear_line.append(line.string)
                if clear_line:
                    clear_data.append(clear_line)

            wh = Warehouse.objects.get_or_create(short_name=options["warh"])[0]
            for tr in clear_data:
                try:
                    f7 = float(tr[7])
                except ValueError:
                    f7 = 0
                if tr[8] == 'нет':
                    pbc = False
                else:
                    pbc = True
                Transaction.objects.get_or_create(
                    warh=wh,
                    cod=tr[0],
                    datetime=datetime.strptime(tr[1]+'+0700', '%Y.%m.%d %H:%M:%S%z'),
                    target=tr[2],
                    org=Organizer.objects.get_or_create(username=tr[3])[0],
                    purchase_title=tr[4],
                    user=Username.objects.get_or_create(username=tr[5])[0],
                    fare=float(tr[6].replace(',', '.')),
                    paid=f7,
                    paid_by_card=pbc,
                    fine=float(tr[9].replace(',', '.'))
                )

            if(decreases):
                for i in decreases.items():
                    r = ReductionFine(
                        transact=Transaction.objects.get(cod=i[0]),
                        amount=i[1]
                    )
                    r.save()
        os.remove(f'./reports/xls/{options["warh"]}/daily/{options["filename"]}')
        return True