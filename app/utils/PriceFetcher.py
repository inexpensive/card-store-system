import re
from forex_python.converter import CurrencyRates
import requests
from bs4 import BeautifulSoup


def round_price(price):
    if price < 0.3:
        price = 0.25
    elif price < 0.55:
        price = 0.5
    elif price < 0.8:
        price = 0.75
    elif price < 5:
        price = round(price * 10) / 10 - 0.01
    elif price < 10:
        price = round(price * 2) / 2 - 0.01
    elif price < 50:
        price = round(price) - 0.01
    else:
        price = round(price / 5.0) * 5 - 0.01
    return price


def get_price_markup_from_mtg_goldfish(url):
    url += '#paper'
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'lxml')
        table = soup.find('table', class_='table-bordered')
        table_rows = table.find_all('tr')
        return table_rows[1:]
    else:
        return []


def get_mtg_goldfish_set_code_exception(set):
    exceptions = {
        'MPS_AKH': 'MS3',
    }
    if set in exceptions.keys():
        return exceptions[set]
    else:
        return set


class PriceFetcher:
    def __init__(self):
        self.exchange_rate = None
        self.update_rate()

    def update_rate(self):
        c = CurrencyRates()
        self.exchange_rate = c.get_rate('USD', 'CAD')

    def convert_to_cad(self, price):
        return price * self.exchange_rate

    def get_set_prices(self, set, price_adjustment=1, foil=False):
        set = get_mtg_goldfish_set_code_exception(set)
        url = 'https://www.mtggoldfish.com/index/{0}'.format(set)
        if foil:
            url += '_F'
        table_rows = get_price_markup_from_mtg_goldfish(url)
        prices = self.get_prices_from_table_rows(table_rows, price_adjustment)
        return prices

    @staticmethod
    def apply_condition_multiplier(price, condition):
        if condition == 'SP':
            price = price * 0.9
        elif condition == 'MP':
            price = price * 0.75
        elif condition == 'HP':
            price = price * 0.5
        return price

    def get_prices_from_table_rows(self, table_rows, price_adjustment):
        prices = {}
        for row in table_rows:
            name = row.find('a').text
            price = self.convert_to_cad(float(re.sub('[\n,]', '', row.find('td', class_='text-right').text))) * price_adjustment
            price_by_condition = self.get_condition_prices_tuple(price)
            prices[name] = price_by_condition
        return prices

    def get_condition_prices_tuple(self, price):
        nm_price = round_price(price)
        sp_price = round_price(self.apply_condition_multiplier(price, 'SP'))
        mp_price = round_price(self.apply_condition_multiplier(price, 'MP'))
        hp_price = round_price(self.apply_condition_multiplier(price, 'HP'))
        price_by_condition = (nm_price, sp_price, mp_price, hp_price)
        return price_by_condition



