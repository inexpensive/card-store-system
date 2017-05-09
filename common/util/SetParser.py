import json

from django.http import HttpResponse, HttpResponseNotFound

from inventory.models import MagicSet

"""
Requires the AllSets.json file from www.mtgjson.com/json/AllSets.json.zip
"""


def get_set_name(card_set):
    if 'alternativeNames' in card_set.keys():
        set_name = card_set['alternativeNames'][0]
    else:
        set_name = card_set['name']
    return set_name


def parse_all_sets(request):
    if request.user.id == 1:
        with open('AllSets.json') as data_file:
            data = json.load(data_file)
            for key in data.keys():
                card_set = data[key]
                set_name = get_set_name(card_set)
                set_code = card_set['code']
                set_release_date = card_set['releaseDate']
                new_set = MagicSet(name=set_name, code=set_code, release_date=set_release_date)
                new_set.save()
        return HttpResponse('DONE')
    else:
        return HttpResponseNotFound()
