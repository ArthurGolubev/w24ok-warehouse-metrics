import os
from loguru import logger
from datetime import datetime
from bs4 import BeautifulSoup
from main.models import Prolongation
from main.models import Warehouse, Username, Organizer, Transaction, ReductionFine
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Очистка данных из скачанного отчёта и вставка их в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('warh')
        parser.add_argument('filename')
        parser.add_argument('end')

    @logger.catch
    def handle(self, *args, **options):
        logger.info(f"FN2 -> {options['filename']}")
        with open(f'./reports/xls/{options["warh"]}/archive/{options["filename"]}', 'r') as f:
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
                                logger.info('case 1')
                                prolongation[rows[i-2].find_all('td')[0].string] = line.string.strip()
                            else:
                                logger.info('case 2')
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
                except TypeError:
                    f7 = 0

                # Обработка повреждённых данных
                if tr[3] == None:
                    tr[3] = 'X'
                if tr[4] == None:
                    tr[4] = 'X'
                if tr[5] == None:
                    tr[5] = 'X'

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
            if(prolongation):
                for i in prolongation.items():
                    p = Prolongation(
                        transact=Transaction.objects.get(cod=i[0]),
                        reason=i[1]
                    )
                    p.save()
            w = Warehouse.objects.get(short_name=options["warh"])
            w.last_download_date=datetime.strptime(options['end'], '%d.%m.%Y')
            if w.end_date_download == datetime.strptime(options['end'], '%d.%m.%Y').date():
                logger.debug("OK")
                w.download_status=False
            w.save()
        os.remove(f'./reports/xls/{options["warh"]}/archive/{options["filename"]}')
        return True