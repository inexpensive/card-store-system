import json
import os
from urllib.request import urlretrieve
import time
import datetime
from app.utils.Database import Database
from bs4 import BeautifulSoup
import requests
import re

"""
Requires the AllSets.json file from www.mtgjson.com/json/AllSets.json.zip
"""
start_time = time.time()
start_time_string = datetime.datetime.fromtimestamp(int(start_time)).strftime('%Y-%m-%d %H:%M:%S')
print("start time: {0}".format(start_time_string))
# create a database connection
path = os.path.abspath('../config.yaml')
db = Database(path)


def get_types(card):
    keys = card.keys()
    supertypes_array = []
    if 'supertypes' in keys:
        supertypes_array = card['supertypes']
    types_array = []
    if 'types' in keys:
        types_array = card['types']
    subtypes_array = []
    if 'subtypes' in keys:
        subtypes_array = card['subtypes']
    supertypes_json = json.dumps(supertypes_array)
    types_json = json.dumps(types_array)
    subtypes_json = json.dumps(subtypes_array)
    return supertypes_json, types_json, subtypes_json


def get_color(card):
    color_array = ['Colorless']
    if 'colors' in card.keys():
        color_array = card['colors']
    return json.dumps(color_array)


def get_card_text(card):
    keys = card.keys()
    rules_text = ''
    if 'text' in keys:
        rules_text = card['text']
    flavor_text = ''
    if 'flavor' in keys:
        flavor_text = card['flavor']
    return rules_text, flavor_text


def get_power_and_toughness(card):
    power = 0
    toughness = 0
    if 'power' in card.keys():
        power = card['power']
        toughness = card['toughness']
    return power, toughness


def download_image(name, card):
    multiverse_id = ''
    image_path = os.path.abspath('../images/None/no_art.jpg')
    if 'multiverseid' in card.keys():
        multiverse_id = card['multiverseid']
        # noinspection PyPep8Naming
        image_URL = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid={0}&type=card'.format(multiverse_id)
        image_path = os.path.abspath('../images/{0}/{1}_{2}.jpg'.format(card_set_code, name.replace(' ', '_'), multiverse_id))
        directory = os.path.dirname(image_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        urlretrieve(image_URL, image_path)
        image_path = re.search("/images.*", image_path).group(0)
    return multiverse_id, image_path


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


def get_price(set_name, card_name, is_foil, collectors_number):
    price = -1
    set_name = convert_to_mtg_goldfish(set_name)
    card_name = convert_to_mtg_goldfish(card_name)
    if is_basic_land(card_name):
        card_name += "-{0}".format(collectors_number)
    foil_modifier = ""
    if is_foil:
        foil_modifier = ":Foil"
    url = "https://www.mtggoldfish.com/price/{0}{1}/{2}".format(set_name, foil_modifier, card_name)
    r = requests.get(url)
    if r.status_code == 200:
        try:
            soup = BeautifulSoup(r.content, "lxml")
            price_box_paper = soup.find("div", class_="price-box paper")
            price = float(price_box_paper.find("div", class_="price-box-price").text)
        except AttributeError:
            price = -1
    return price


def get_mana_cost(card):
    mana_cost = ''
    cmc = 0
    if 'manaCost' in card.keys():
        mana_cost = card['manaCost']
        cmc = card['cmc']
    return mana_cost, cmc


def get_color_identity(card):
    if 'colorIdentity' in card.keys():
        color_identity = card['colorIdentity']
    else:
        color_identity = ['C']
    return json.dumps(color_identity)

# TODO: add card condition!!!!
with open('AllSets.json') as data_file:
    data = json.load(data_file)
    card_set = data['KLD']
    card_set_name = card_set['name']
    card_set_code = card_set['code']
    cards = card_set['cards']
    for card in cards:
        name = card['name']
        supertypes, types, subtypes = get_types(card)
        mana_cost, cmc = get_mana_cost(card)
        color = get_color(card)
        color_identity = get_color_identity(card)
        rarity = card['rarity'][0]
        artist = card['artist']
        rules_text, flavor_text = get_card_text(card)
        power, toughness = get_power_and_toughness(card)
        collector_number = card['number']
        multiverse_id, image_path = download_image(name, card)
        stock = 0
        language = 'en'
        foil_possibilities = (False, True)
        for foil in foil_possibilities:
            price = get_price(card_set_name, name, foil, collector_number)
            db.insert_card(name, card_set_code, language, foil, supertypes, types, subtypes, mana_cost, cmc, color,
                           rarity, artist, rules_text, flavor_text, power, toughness, collector_number, multiverse_id,
                           image_path, stock, price, color_identity)

finish_time = time.time()
finish_time_string = datetime.datetime.fromtimestamp(int(finish_time)).strftime('%Y-%m-%d %H:%M:%S')
print("finish time: {0}".format(finish_time_string))
print("--- {0} seconds ---".format(finish_time - start_time))
