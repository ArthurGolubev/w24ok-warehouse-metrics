import os
import requests
import redis

from time import sleep
from loguru import logger
from bs4 import BeautifulSoup
from selenium import webdriver
from ReportError import ReportError
from datetime import datetime, timedelta
from pathlib import Path

class Report:
    
    
    def __init__(self, period=None) -> None:
        
        self.warh = os.getenv('WARH')
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.page_load_strategy = 'eager'
        self.download_path = f'/data/cache/{self.warh}'
        Path(self.download_path).mkdir(exist_ok=True)
        # options.add_experimental_option('prefs', {"download.default_directory" : self.download_path})
        # self.browser    = webdriver.Chrome(executable_path='/celery_app/chromedriver', options=options)
        self.browser = webdriver.Remote(command_executor='http://selenium-svc:4444/wd/hub', options=options)
        # self.browser.set_page_load_timeout(120)
        # self.browser.set_script_timeout(120)
        self.clear_data_ = []
        self.period=period
        self.decreases = {}
        self.prolongations = {}
        self.task_name = f'task {self.warh}'



    # @logger.catch
    def get_report(self):
        logger.info(f'\n<b>{self.task_name}</b>\n<i>Process start</i>\nPeriod:\n{self.period}\n#w24ok #Reports')
        try:
            self.browser.get('https://store.24-ok.ru/site/login')
            login = self.browser.find_element('xpath' ,'//input[@id="loginform-username"]')
            password = self.browser.find_element('xpath', '//input[@id="loginform-password"]')
            button = self.browser.find_element('xpath', '//button[@name="login-button"]')
            login.send_keys(os.getenv(f'{self.warh}0'))
            password.send_keys(os.getenv(f'{self.warh}1'))
            button.click()
            sleep(5)
            self.browser.get('https://store.24-ok.ru/report/issue')
            sleep(5)
            if self.period:
                date_start = self.browser.find_element("xpath", "//input[@id='filterreport-date_start']")
                date_end = self.browser.find_element("xpath", "//input[@id='filterreport-date_end']")
                create_button_elem = self.browser.find_element("xpath", "//button[@value='create']")
                date_start.clear()
                date_end.clear()
                date_end.send_keys(self.period["end"].strftime('%d.%m.%Y'))
                date_start.send_keys(self.period["start"].strftime('%d.%m.%Y'))
                create_button_elem.click()
                sleep(10)
            load_button_elem = self.browser.find_element("xpath", "//button[@value='xls']")
            logger.info(f'{load_button_elem=}')
            load_button_elem.click()
            download = False
            today = datetime.today()
            y = today.year
            m = today.month
            d = today.day
            if m < 10: m = f'0{m}'
            if d < 10: d = f'0{d}'
            start_time = datetime.now()
            # Тут проверку можно переработать на CronJob из Kubernetes
            while(not download and not (datetime.now() > start_time + timedelta(minutes=3))):
                sleep(5)
                for file_ in os.listdir(self.download_path):
                    if file_.startswith(f'Data-{y}{m}{d}') and file_.endswith('.xls'):
                        download = True
                        self.filename = file_
                        self.browser.get('https://store.24-ok.ru/site/logout')
        except Exception as e:
            raise ReportError(where='get_report', Traceback=e, period=self.period)
        finally:
            sleep(15)
            self.browser.quit()


    # @logger.catch
    def clear_data(self):
        try:
            with open(f'{self.download_path}/{self.filename}', 'r') as f:
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
            return
            self.remove_files()


    # @logger.catch
    def send_data(self):
        try:
            username = os.getenv("REPORT_USERNAME")
            password = os.getenv("REPORT_PASSWORD")
            endpoint = os.getenv("ENDPOINT_GRAPHQL")
            
            # Get Token ---------------------
            with open('/celery_app/handler/schema/GET_TOKEN.gql') as gql: mutation = f"""\n""".join(gql.readlines())
            r = requests.post(endpoint, json={"query": mutation, "variables": {"username": username, "password": password}})
            if not r.status_code == 200 or r.json().get('errors'):
                raise ReportError(where='send_data / TOKEN', message=r.json(), period=self.period)
            
            # Push Transaction --------------
            token = r.json()['data']['tokenAuth']['token']
            headers = {"Authorization": f"JWT {token}"}
            with open('/celery_app/handler/schema/PUSH_TRANSACTIONS.gql') as gql: mutation = f"""\n""".join(gql.readlines())
            r = requests.post(endpoint, json={"query": mutation, "variables": {"warh": self.warh, "clearData": self.clear_data_}}, headers=headers)
            if not r.status_code == 200 or r.json().get('errors'):
                raise ReportError(where='send_data / Transaction', message=r.json(), period=self.period)
            
            # Push Decreases ----------------
            if self.decreases.items():
                logger.info(f'got decreases: {self.decreases.items()}\nPeriod:\n{self.period}')
                with open('/celery_app/handler/schema/PUSH_DECREASES.gql') as gql: mutation = f"""\n""".join(gql.readlines())
                r = requests.post(endpoint, json={"query": mutation, "variables": {"decreases": list(self.decreases.items()), "warh": self.warh }}, headers=headers)
                if not r.status_code == 200 or r.json().get('errors'):
                    raise ReportError(where='send_data / Decreases', message=r.json(), period=self.period)
            
            # Push Prolongations -------------
            if self.prolongations.items():
                logger.info(f'got prolongations: {self.decreases.items()}\nPeriod:\n{self.period}')
                with open('/celery_app/handler/schema/PUSH_PROLONGATIONS.gql') as gql: mutation = f"""\n""".join(gql.readlines())
                r = requests.post(endpoint, json={"query": mutation, "variables": {"prolongations": list(self.prolongations.items()), "warh": self.warh }}, headers=headers)
                if not r.status_code == 200 or r.json().get('errors'):
                    raise ReportError(where='send_data / Prolongation', message=r.json(), period=self.period)
            if self.period: redis.Redis(host='redis-service-node-port', port='6379', db='0').hmset(f"{self.warh}", {"start": self.period["end"].strftime("%Y/%m/%d")} )
            logger.success(f'\n<b>{self.task_name}</b>\n<i>Process end</i>\nPeriod:\n{self.period}\n#w24ok #Reports')

        except Exception as e:
            raise ReportError(where='send_data', Traceback=e, period=self.period)
        


    @staticmethod
    def remove_files():
        """Удаление файла отчёта"""
        warh = os.getenv('WARH')
        for file_ in os.listdir(f'/data/cache/{warh}'):
            if file_.endswith('.xls'):
                os.remove(f'/data/cache/{warh}/{file_}')

