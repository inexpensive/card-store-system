import datetime
import os
from app.utils.Database import Database
import re
from forex_python.converter import CurrencyRates
import requests
from bs4 import BeautifulSoup
import time

start_time = time.time()
start_time_string = datetime.datetime.fromtimestamp(int(start_time)).strftime('%Y-%m-%d %H:%M:%S')
print("start time: {0}".format(start_time_string))

# create a database connection
path = os.path.abspath('../../config.yaml')
db = Database(path)

cards = db.get_cards()


def convert_to_mtg_goldfish(name):
    name = name.replace("'", "")
    name = name.replace(",", " ")
    name = re.sub("\s+", "+", name)
    return name


def is_basic_land(card_name):
    basic_lands = (
        "Plains",
        "Island",
        "Swamp",
        "Mountain",
        "Forest",
    )
    return card_name in basic_lands


def get_price_from_mtg_goldfish(url):
    r = requests.get(url)
    try:
        soup = BeautifulSoup(r.content, 'lxml')
        price_box_paper = soup.find("div", class_="price-box paper")
        price = float(price_box_paper.find("div", class_="price-box-price").text)
    except AttributeError:
        price = -1
    return price


def convert_to_cad(price, rate):
    return price * rate


def get_usd_to_cad_exchange_rate():
    c = CurrencyRates()
    return c.get_rate('USD', 'CAD')


def update_price(card):
    card_name = convert_to_mtg_goldfish(card[0])
    is_foil = card[1]
    set_name = convert_to_mtg_goldfish(card[2])
    collector_number = card[3]
    if is_basic_land(card_name):
        card_name += "-{0}".format(collector_number)
    foil_modifier = ''
    if is_foil:
        foil_modifier = ":Foil"
    url = "https://www.mtggoldfish.com/price/{0}{1}/{2}".format(set_name, foil_modifier, card_name)
    price = get_price_from_mtg_goldfish(url)
    rate = get_usd_to_cad_exchange_rate()
    price = convert_to_cad(price, rate)
    return price


for card in cards:
    price = update_price(card)
    db.update_price(price, card)

finish_time = time.time()
finish_time_string = datetime.datetime.fromtimestamp(int(finish_time)).strftime('%Y-%m-%d %H:%M:%S')
print("finish time: {0}".format(finish_time_string))
print("--- {0} seconds ---".format(finish_time - start_time))