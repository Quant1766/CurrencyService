import requests
import datetime

from Currency.models import Currency

"""
api doc https://bank.gov.ua/ua/open-data/api-dev
today currency   https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json
by date currency https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json&date=19960106


"""
URL_REQUEST = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'


def get_catalog_by_date(date_str: str):
    url = f'{URL_REQUEST}&date={date_str}' if date_str else URL_REQUEST

    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    return []


def update_catalog_by_date(date_str: str):
    data = get_catalog_by_date(date_str)
    data_objs = [Currency(r030=d['r030'], txt=d['txt'], rate=d['rate'], cc=d['cc'], exchangedate=datetime.datetime.strptime(d['exchangedate'], '%d.%m.%Y')) for d in data]
    # Currency.objects.bulk_create(data_objs, ignore_conflicts=True)
