import json
import os
from app.utils.Database import Database

"""
Requires the AllSets.json file from www.mtgjson.com/json/AllSets.json.zip
"""

# create a database connection
path = os.path.abspath('../config.yaml')
db = Database(path)


def get_set_name(card_set):
    if 'alternativeNames' in card_set.keys():
        set_name = card_set['alternativeNames'][0]
    else:
        set_name = card_set['name']
    return set_name


with open('AllSets.json') as data_file:
    data = json.load(data_file)
    for key in data.keys():
        card_set = data[key]
        set_name = get_set_name(card_set)
        set_code = card_set['code']
        set_release_date = card_set['releaseDate']
        set_number_of_cards = card_set['cards'].__len__()
        db.insert_set(set_name, set_code, set_release_date, set_number_of_cards)



