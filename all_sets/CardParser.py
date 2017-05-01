import json
import os
from urllib.request import urlretrieve
import time
import datetime
from app.utils.Database import Database
import re

from app.utils.PriceFetcher import PriceFetcher

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
    return supertypes_array, types_array, subtypes_array


def convert_color_to_single_character(color):
    if color == 'Blue':
        color = 'U'
    else:
        color = color[0]
    return color


def join_with_spaces(color_array):
    return ' '.join(color_array)


def get_color(card):
    color_array = ['C']
    color_text = 'Colorless'
    if 'colors' in card.keys():
        color_array = card['colors']
        color_text = join_with_spaces(color_array)
    for i in range(color_array.__len__()):
        color_array[i] = convert_color_to_single_character(color_array[i])
    return color_array, color_text


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
    image_path = os.path.abspath('../inventory/static/images/None/no_art.jpg')
    if 'multiverseid' in card.keys():
        multiverse_id = card['multiverseid']
        image_path = os.path.abspath(
            '../inventory/static/images/{0}/{1}_{2}.jpg'.format(card_set_code, name.replace(' ', '_'), multiverse_id))
        if not os.path.exists(image_path):
            directory = os.path.dirname(image_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            image_URL = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid={0}&type=card'.format(
                multiverse_id)
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


def get_card_price(card_name, condition, price_dict):
    if card_name not in price_dict.keys():
        price = -1
    else:
        price_by_condition = price_dict[card_name]
        if condition == 'NM':
            price = price_by_condition[0]
        elif condition == 'SP':
            price = price_by_condition[1]
        elif condition == 'MP':
            price = price_by_condition[2]
        else:
            price = price_by_condition[3]
    return price


def get_price(card_name, is_foil, layout_type, is_focal_card, ordered_card_names, condition, non_foil_prices,
              foil_prices):
    if layout_type == 'split' or layout_type == 'aftermath':
        if is_focal_card:
            if card_name != 'Who':
                card_name = ordered_card_names[0] + ' // ' + ordered_card_names[1]
            else:
                card_name = 'Who/What/When/Where/Why'
    if is_foil:
        price = get_card_price(card_name, condition, foil_prices)
    else:
        price = get_card_price(card_name, condition, non_foil_prices)
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
    return color_identity


def get_layout_type(card):
    layout_type = card['layout']
    if layout_type == 'normal':
        ordered_card_names = []
        is_focal_card = True
    else:
        ordered_card_names = card['names']
        if card['name'] == ordered_card_names[0]:
            is_focal_card = True
        else:
            is_focal_card = False
    return layout_type, ordered_card_names, is_focal_card


with open('AllSets.json') as data_file:
    data = json.load(data_file)
    card_sets = ['AER', 'AKH', 'BFZ', 'EMN', 'KLD', 'MM3', 'OGW', 'SOI']
    for set_ in card_sets:
        card_set = data[set_]
        card_set_code = card_set['code']
        price_fetcher = PriceFetcher()
        non_foil_prices = price_fetcher.get_set_prices(card_set_code)
        foil_prices = price_fetcher.get_set_prices(card_set_code, foil=True)
        cards = card_set['cards']
        for card in cards:
            name = card['name']
            supertypes, types, subtypes = get_types(card)
            supertypes_text = join_with_spaces(supertypes)
            types_text = join_with_spaces(types)
            subtypes_text = join_with_spaces(subtypes)
            mana_cost, cmc = get_mana_cost(card)
            color, color_text = get_color(card)
            color_identity = get_color_identity(card)
            rarity = card['rarity'][0]
            artist = card['artist']
            rules_text, flavor_text = get_card_text(card)
            power, toughness = get_power_and_toughness(card)
            collector_number = card['number']
            layout_type, ordered_card_names, is_focal_card = get_layout_type(card)
            multiverse_id, image_path = download_image(name, card)
            stock = 0
            language = 'en'
            foil_possibilities = (False, True)
            for foil in foil_possibilities:
                for condition in ('NM', 'SP', 'MP', 'HP'):
                    price = get_price(name, foil, layout_type, is_focal_card, ordered_card_names, condition,
                                      non_foil_prices, foil_prices)
                    print(name + ' - ' + condition + ' - ' + str(foil) + ' - ' + str(price))
                    db.insert_card(name, card_set_code, language, foil, supertypes, types, subtypes, mana_cost, cmc, color,
                                   rarity, artist, rules_text, flavor_text, power, toughness, collector_number,
                                   multiverse_id, image_path, stock, price, color_identity, layout_type,
                                   ordered_card_names, is_focal_card, condition, supertypes_text, types_text, subtypes_text,
                                   color_text)
            print('inserted ' + name)
    db.update_database()

finish_time = time.time()
finish_time_string = datetime.datetime.fromtimestamp(int(finish_time)).strftime('%Y-%m-%d %H:%M:%S')
print("finish time: {0}".format(finish_time_string))
print("--- {0} seconds ---".format(finish_time - start_time))
