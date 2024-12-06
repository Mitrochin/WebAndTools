import asyncio
from currency_service import CurrencyService
from utils import ensure_log_directory


async def main(days_count: int, additional_currencies=None):
    # Проверка существования логов (Checking for the existence of logs)
    ensure_log_directory()

    if additional_currencies is None:
        additional_currencies = ['EUR', 'USD']

    service = CurrencyService()

    # Получение курса валют (Fetching exchange rates)
    rates_data = await service.get_exchange_rates(days_count)

    # Фильтрация курса валют по предоставленным валютам (Filtering exchange rates based on provided currencies)
    filtered_rates = service.filter_exchange_rates(rates_data, additional_currencies)

    return filtered_rates


if __name__ == '__main__':
    import sys

    # Проверка количества дней (Checking if the number of days is provided as an argument)
    if len(sys.argv) < 2:
        print("Please provide the number of days as an argument")
    else:
        days = int(sys.argv[1])
        if days > 10:
            print("Number of days cannot be more than 10")
        else:
            # Разбор дополнительных валют (Parse additional currencies)
            additional_currencies_argument = sys.argv[2].split(',') if len(sys.argv) > 2 else ['EUR', 'USD']
            rates = asyncio.run(main(days, additional_currencies_argument))
            print(rates)
