import os
import redis
import requests

from loguru import logger
from bs4 import BeautifulSoup


from ReportError import ReportError
from datetime import datetime
from pathlib import Path

class Report:
    
    
    def __init__(self, period=None) -> None:
        
        self.warh = os.getenv('WARH')
        self.download_path = f'/data/cache/{self.warh}'
        Path(self.download_path).mkdir(parents=True, exist_ok=True)
        self.clear_data_ = []
        self.period=period
        self.decreases = {}
        self.prolongations = {}
        self.task_name = f'task {self.warh}'



    def get_report(self):
        logger.info(f'\n<b>{self.task_name}</b>\n<i>Process start</i>\nPeriod:\n{self.period}\n#w24ok #Reports')
        today = datetime.today()
        with requests.Session() as session:
            login_url = 'https://store.24-ok.ru/site/login'
            logout_url = 'https://store.24-ok.ru/site/logout'

            if self.period:
                end = self.period["end"]
                start = self.period["start"]
            else:
                end = today.strftime('%d.%m.%Y')
                start = today.strftime('%d.%m.%Y')
            issue = f'https://store.24-ok.ru/report/issue?FilterReport%5Bdate_start%5D={start}&FilterReport%5Bdate_end%5D={end}&soffice=60&button=xls'
            
            response = session.get(login_url) # 1. захожу, чтобы получить csrf
            soup = BeautifulSoup(response.content, 'html.parser')
            csrf = soup.find('input', {'name': '_csrf'})['value']

            payload_data = {
                "_csrf": csrf,
                "LoginForm[username]": os.getenv(f'{self.warh}0'),
                "LoginForm[password]": os.getenv(f'{self.warh}1')
            }

            session.post(login_url, data=payload_data) # 2. отправляю форму с данными
            
            resp3 = session.get(issue) # 3. отправляю запрос на скачивание документа .xls
            y = today.year
            m = today.month
            d = today.day
            if m < 10: m = f'0{m}'
            if d < 10: d = f'0{d}'
            self.filename = f'Data-{y}{m}{d}-{self.warh}.xls'
            with open(os.path.join(self.download_path, self.filename), 'wb') as f:
                f.write(resp3.content)
                logger.info(f'{resp3.text=}')

            session.get(logout_url) # 4. разлогиниваюсь на сайте


    def clear_data(self):
        logger.info('start clear_data')
        try:
            with open(os.path.join(self.download_path, self.filename), 'r') as f:
                soup = BeautifulSoup(f, 'html.parser')
                rows = soup.find_all('tr')
                
                for i, row in enumerate(rows):
                    raw_line = row.find_all('td')
                    clear_line = []
                    for line in raw_line:
                        if line.get('colspan'):
                            if line.get('colspan') == '1':
                                self.decreases[rows[i-1].find_all('td')[0].string] = line.string.replace('- ', '').strip()
                            elif line.get('colspan') == '5':
                                if rows[i-1].find_all('td')[0].string.strip() ==  "В том числе с уменьшением штрафа":
                                    self.prolongations[rows[i-2].find_all('td')[0].string] = line.string.strip()
                                else:
                                    self.prolongations[rows[i-1].find_all('td')[0].string] = line.string.strip()
                        else:
                            # Broken data
                            if line.string == None: line_ = '' 
                            else: line_ = line.string
                            clear_line.append(line_)
                    if clear_line:
                        self.clear_data_.append(clear_line)
                return True
        except Exception as e:
            raise ReportError(where='clear_data', Traceback=e, period=self.period)
        finally:
            self.remove_files()
            logger.success('remove files')


    def send_data(self):
        logger.info('start send_data')
        try:
            username = os.getenv("REPORT_USERNAME")
            password = os.getenv("REPORT_PASSWORD")
            endpoint = os.getenv("ENDPOINT_GRAPHQL")
            
            # Get Token ---------------------
            with open('/w24ok_reports/schema/GET_TOKEN.gql') as gql: mutation = f"""\n""".join(gql.readlines())
            r = requests.post(endpoint, json={"query": mutation, "variables": {"username": username, "password": password}})
            if not r.status_code == 200 or r.json().get('errors'):
                raise ReportError(where='send_data / TOKEN', message=r.json(), period=self.period)
            
            # Push Transaction --------------
            token = r.json()['data']['tokenAuth']['token']
            headers = {"Authorization": f"JWT {token}"}
            with open('/w24ok_reports/schema/PUSH_TRANSACTIONS.gql') as gql: mutation = f"""\n""".join(gql.readlines())
            r = requests.post(endpoint, json={"query": mutation, "variables": {"warh": self.warh, "clearData": self.clear_data_}}, headers=headers)
            logger.warning(f'{r.text=}')
            if not r.status_code == 200 or r.json().get('errors'):
                raise ReportError(where='send_data / Transaction', message=r.json(), period=self.period)
            
            # Push Decreases ----------------
            if self.decreases.items():
                logger.info(f'got decreases: {self.decreases.items()}\nPeriod:\n{self.period}')
                with open('/w24ok_reports/schema/PUSH_DECREASES.gql') as gql: mutation = f"""\n""".join(gql.readlines())
                r = requests.post(endpoint, json={"query": mutation, "variables": {"decreases": list(self.decreases.items()), "warh": self.warh }}, headers=headers)
                if not r.status_code == 200 or r.json().get('errors'):
                    raise ReportError(where='send_data / Decreases', message=r.json(), period=self.period)
            
            # Push Prolongations -------------
            if self.prolongations.items():
                logger.info(f'got prolongations: {self.decreases.items()}\nPeriod:\n{self.period}')
                with open('/w24ok_reports/schema/PUSH_PROLONGATIONS.gql') as gql: mutation = f"""\n""".join(gql.readlines())
                r = requests.post(endpoint, json={"query": mutation, "variables": {"prolongations": list(self.prolongations.items()), "warh": self.warh }}, headers=headers)
                if not r.status_code == 200 or r.json().get('errors'):
                    raise ReportError(where='send_data / Prolongation', message=r.json(), period=self.period)
            if self.period: redis.Redis(host='redis-svc', port='6379', db='0').hmset(f"{self.warh}", {"start": self.period["end"].strftime("%Y/%m/%d")} )
            logger.success(f'\n<b>{self.task_name}</b>\n<i>Process end</i>\nPeriod:\n{self.period}\n#w24ok #Reports')

        except Exception as e:
            logger.info(f'{e=}')
            raise ReportError(where='send_data', Traceback=e, period=self.period)
        


    @staticmethod
    def remove_files():
        """Удаление файла отчёта"""
        warh = os.getenv('WARH')
        for file_ in os.listdir(f'/data/cache/{warh}'):
            if file_.endswith('.xls'):
                os.remove(f'/data/cache/{warh}/{file_}')

