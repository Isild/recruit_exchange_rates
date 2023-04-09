import requests
from decouple import config
from datetime import date


def get_historical_day_exchange_rate(data_date: date):
    data_date = data_date.strftime("%Y-%m-%d")

    url = config('EXCHANGE_RATE_SERVICE_URL') + "historical/" + \
        data_date + ".json?app_id=" + config('KEY_CODE')
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Problem with get exchange rate.")

    return response


def get_current_day_exchange_rate():
    url = config('EXCHANGE_RATE_SERVICE_URL') + \
        "latest.json?app_id=" + config('KEY_CODE')
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Problem with get exchange rate.")

    return response
