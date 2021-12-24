from django.core.management.base import BaseCommand

from Currency.utils import update_catalog_by_date
import datetime
import aiohttp
import asyncio

from Currency.models import Currency

"""
api doc https://bank.gov.ua/ua/open-data/api-dev
today currency   https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json
by date currency https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json&date=19960106


"""
URL_REQUEST = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'


class Command(BaseCommand):
    help = 'Init catalog'

    async def fetch(self, client, date_str):
        async with client.get(f'{URL_REQUEST}&date={date_str}') as resp:
            assert resp.status == 200
            return await resp.json()

    async def parse(self):
        async with aiohttp.ClientSession() as client:
            first_date = datetime.date(1996, 1, 6)
            output_l = []
            duration = datetime.datetime.now().date() - first_date
            for d in range(duration.days-10, duration.days):
                day = first_date + datetime.timedelta(days=d)
                data = await self.fetch(client, day.strftime('%Y%m%d'))
                data_objs = [Currency(r030=d['r030'], txt=d['txt'], rate=d['rate'], cc=d['cc'], exchangedate=day) for d
                             in data]
                output_l += data_objs
            return output_l

    def handle(self, *args, **options):
        loop = asyncio.get_event_loop()
        data_objs = loop.run_until_complete(self.parse())
        Currency.objects.bulk_create(data_objs, ignore_conflicts=True)
