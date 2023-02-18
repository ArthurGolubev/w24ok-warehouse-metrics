import json
from loguru import logger
from main.models import Warehouse
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Очистка данных из скачанного отчёта и вставка их в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('warh')
    
    @logger.catch
    def handle(self, *args, **options):
        w = Warehouse.objects.get_or_create(short_name=options["warh"])[0]
        return json.dumps({
            "download_status": w.download_status,
            "start_date_download": f"{w.start_date_download}",
            "last_download_date": f"{w.last_download_date}",
            "end_date_download": f"{w.end_date_download}",
        })