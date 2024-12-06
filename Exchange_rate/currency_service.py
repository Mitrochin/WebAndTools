import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)


class PrivatBankAPIClient:
    BASE_URL = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='

    async def fetch_exchange_rates(self, session, date: str):
        # Получение курса валют (Getting the exchange rate)
        url = f'{self.BASE_URL}{date}'
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                logging.error(f'Failed to fetch exchange rates for {date}. Status: {response.status}')
                return None


class CurrencyService:
    def __init__(self):
        self.client = PrivatBankAPIClient()

    @staticmethod
    def get_dates(days: int):
        # Получение дат, для получения курса валют (Getting dates for getting exchange rates)
        dates = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y')
            dates.append(date)
        return dates

    async def get_exchange_rates(self, days: int):
        # Получение курса валют по датам (Getting exchange rates by dates)
        dates = self.get_dates(days)
        async with aiohttp.ClientSession() as session:
            tasks = [self.client.fetch_exchange_rates(session, date) for date in dates]
            results = await asyncio.gather(*tasks)
        return results

    @staticmethod
    def filter_exchange_rates(rates, currencies):
        filtered_rates = []
        for rate in rates:
            filtered_rate = {}
            if rate:
                date = rate.get("date")
                if date:
                    filtered_rate[date] = {}
                    for currency in currencies:
                        filtered_currency = next((item for item in rate['exchangeRate'] if item["currency"] == currency), None)
                        if filtered_currency:
                            filtered_rate[date][currency] = {
                                "sale": filtered_currency["saleRate"],
                                "purchase": filtered_currency["purchaseRate"]
                            }
                    filtered_rates.append(filtered_rate)
        return filtered_rates

#
