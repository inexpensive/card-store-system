from app.utils.CardOps import is_basic_land
import re
from forex_python.converter import CurrencyRates
import requests
from bs4 import BeautifulSoup


class PriceFetcher:
    def __init__(self):
        self.exchange_rate = None
        self.update_rate()

    def update_rate(self):
        c = CurrencyRates()
        self.exchange_rate = c.get_rate('USD', 'CAD')

    @staticmethod
    def convert_to_mtg_goldfish(name):
        name = name.replace("'", '')
        name = name.replace(',', ' ')
        name = re.sub('\s+', '+', name)
        return name

    def get_price_from_mtg_goldfish(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            try:
                soup = BeautifulSoup(r.content, 'lxml')
                price_box_paper = soup.find('div', class_='price-box paper')
                price = float(price_box_paper.find('div', class_='price-box-price').text)
            except AttributeError:
                price = -1
        else:
            price = -1
        return self.convert_to_cad(price)

    def convert_to_cad(self, price):
        return price * self.exchange_rate

    def get_price(self, card, price_adjustment=1):
        card_name = self.convert_to_mtg_goldfish(card['name'])
        set_name = self.convert_to_mtg_goldfish(card['set'])
        is_foil = card['is_foil']
        collector_number = card['collector_number']
        condition = card['condition']
        if is_basic_land(card_name):
            card_name += '-{0}'.format(collector_number)
        foil_modifier = ''
        if is_foil:
            foil_modifier = ':Foil'
        url = 'https://www.mtggoldfish.com/price/{0}{1}/{2}'.format(set_name, foil_modifier, card_name)
        price = self.get_price_from_mtg_goldfish(url)
        if condition != 'NM':
            price = self.apply_condition_multiplier(price, condition)
        return price * price_adjustment

    @staticmethod
    def apply_condition_multiplier(price, condition):
        if condition == 'SP':
            price = price * 0.9
        elif condition == 'MP':
            price = price * 0.75
        elif condition == 'HP':
            price = price * 0.5
        return price

