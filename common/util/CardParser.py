import json
import os
import time
import datetime
import platform

import requests
import shutil
import yaml

import re

from django.http import HttpResponse, HttpResponseNotFound

from inventory.models import MagicCard, MagicSet

"""
Requires the AllSets.json file from www.mtgjson.com/json/AllSets.json.zip
"""


def get_types(card, new_card):
    keys = card.keys()
    if 'supertypes' in keys:
        supertypes_array = card['supertypes']
        new_card.super_types = supertypes_array
        new_card.super_types_text = join_with_spaces(supertypes_array)
    if 'types' in keys:
        types_array = card['types']
        new_card.types = types_array
        new_card.types_text = join_with_spaces(types_array)
    if 'subtypes' in keys:
        subtypes_array = card['subtypes']
        new_card.sub_types = subtypes_array
        new_card.sub_types_text = join_with_spaces(subtypes_array)


def convert_color_to_single_character(color):
    if color == 'Blue':
        color = 'U'
    else:
        color = color[0]
    return color


def join_with_spaces(color_array):
    return ' '.join(color_array)


def get_color(card, new_card):
    color_array = ['C']
    color_text = 'Colorless'
    if 'colors' in card.keys():
        color_array = card['colors']
        color_text = join_with_spaces(color_array)
    for i in range(color_array.__len__()):
        color_array[i] = convert_color_to_single_character(color_array[i])
    new_card.color = color_array
    new_card.color_text = color_text


def get_card_text(card, new_card):
    keys = card.keys()
    if 'text' in keys:
        new_card.rules_text = card['text']
    if 'flavor' in keys:
        new_card.flavor_text = card['flavor']


def get_power_and_toughness(card, new_card):
    if 'power' in card.keys():
        new_card.power = card['power']
        new_card.toughness = card['toughness']


def download_image(name, card, card_set_code, new_card):
    if card_set_code == 'CON' and platform.system() == 'Windows':
        card_set_code = 'CONF'
    if 'multiverseid' in card.keys():
        multiverse_id = card['multiverseid']
        new_card.multiverse_id = multiverse_id
        card_name = name.replace(' ', '_')
        card_name = re.sub('[?:%*|"<>.]', '', card_name)  # removes characters not allowed in windows file paths
        image_path = os.path.abspath(
            'inventory/static/images/{0}/{1}_{2}.jpg'.format(card_set_code, card_name, multiverse_id))
        if not os.path.exists(image_path):
            directory = os.path.dirname(image_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            image_url = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid={0}&type=card'.format(
                multiverse_id)
            r = requests.get(image_url, stream=True)
            with open(image_path, 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)
            del r
        image_path = re.search('[/\\\]images.*', image_path).group(0)  # accounts for unix and windows file paths
        image_path = image_path.replace('\\', '/')  # convert windows path to valid html format
        new_card.image = image_path


def get_mana_cost(card, new_card):
    if 'manaCost' in card.keys():
        new_card.mana_cost = card['manaCost']
        new_card.cmc = card['cmc']


def get_color_identity(card, new_card):
    if 'colorIdentity' in card.keys():
        color_identity = card['colorIdentity']
    else:
        color_identity = ['C']
    new_card.color_identity = color_identity


def get_layout_type(card, new_card):
    layout_type = card['layout']
    if layout_type != 'normal':
        if 'names' in card.keys():
            ordered_card_names = card['names']
            new_card.ordered_card_names = ordered_card_names
            if card['name'] != ordered_card_names[0]:
                new_card.is_focal_card = False


def get_number(card, new_card):
    if 'number' in card.keys():
        collector_number = card['number']
    elif 'mciNumber' in card.keys():
        collector_number = card['mciNumber']
        if '4e/en/' in collector_number:
            collector_number = collector_number[6:]
    else:
        collector_number = '0'
    new_card.collector_number = collector_number


def parse_all_cards(request):
    if request.user.id == 1:
        start_time = time.time()
        start_time_string = datetime.datetime.fromtimestamp(int(start_time)).strftime('%Y-%m-%d %H:%M:%S')
        print("start time: {0}".format(start_time_string))

        with open('online_only_sets.yaml') as f:
            online_only_sets = yaml.load(f)

        with open('AllSets.json', encoding='utf8') as data_file:
            data = json.load(data_file)
            card_sets = data.keys()
            for set_ in card_sets:
                card_set = data[set_]
                card_set_code = card_set['code']
                print('starting ' + card_set_code)
                if card_set_code in online_only_sets:
                    print('skipping ' + card_set_code)
                    continue
                cards = card_set['cards']
                for card in cards:
                    new_card = MagicCard()
                    name = card['name']
                    new_card.name = name
                    new_card.set = MagicSet.objects.get(code=card_set_code)
                    get_types(card, new_card)
                    get_mana_cost(card, new_card)
                    get_color(card, new_card)
                    get_color_identity(card, new_card)
                    new_card.rarity = card['rarity'][0]
                    new_card.artist = card['artist']
                    get_card_text(card, new_card)
                    get_power_and_toughness(card, new_card)
                    get_number(card, new_card)
                    get_layout_type(card, new_card)
                    download_image(name, card, card_set_code, new_card)
                    new_card.save()
                print('done with ' + card_set_code)

        finish_time = time.time()
        finish_time_string = datetime.datetime.fromtimestamp(int(finish_time)).strftime('%Y-%m-%d %H:%M:%S')
        print("finish time: {0}".format(finish_time_string))
        print("--- {0} seconds ---".format(finish_time - start_time))
        return HttpResponse('DONE')
    else:
        return HttpResponseNotFound()
