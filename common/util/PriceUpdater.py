from django.http import HttpResponseNotFound, HttpResponse

from common.util.PriceFetcher import PriceFetcher
from inventory.models import MagicSet, MagicCardItem, MagicCard


def update_all_prices(request):
    foil_set_prices, non_foil_set_prices = get_set_prices()
    items = MagicCardItem.objects.all()
    for item in items:
        card = item.card
        set_code = card.set.code
        name = card.name
        condition = item.condition
        if condition == 'NM':
            condition_code = 0
        elif condition == 'SP':
            condition_code = 1
        elif condition == 'MP':
            condition_code = 2
        else:
            condition_code = 3
        foil = item.foil
        if foil:
            if name in foil_set_prices[set_code]:
                item.price = foil_set_prices[set_code][name][condition_code]
            else:
                item.price = -1
        else:
            if name in non_foil_set_prices[set_code]:
                item.price = non_foil_set_prices[set_code][name][condition_code]
            else:
                item.price = -1
        item.save()


def get_set_prices():
    price_fetcher = PriceFetcher()
    sets = MagicSet.objects.all()
    non_foil_set_prices = {}
    foil_set_prices = {}
    for set_ in sets:
        set_code = set_.code
        non_foil_set_prices[set_code] = price_fetcher.get_set_prices(set_code)
        foil_set_prices[set_code] = price_fetcher.get_set_prices(set_code, foil=True)
    return foil_set_prices, non_foil_set_prices


def create_all_prices(request):
    if request.user.id == 1:
        print('starting')
        foil_set_prices, non_foil_set_prices = get_set_prices()
        cards = MagicCard.objects.all()
        for card in cards:
            set_code = card.set.code
            if set_code in non_foil_set_prices:
                prices = non_foil_set_prices[set_code]
                name = card.name
                create_items(card, name, prices, False)
                prices = foil_set_prices[set_code]
                create_items(card, name, prices, True)
                print("done with " + set_code + " == " + name)
        return HttpResponse('DONE')
    else:
        return HttpResponseNotFound()


def create_items(card, name, prices, foil):
    if name in prices:
        create_priced_items(card, name, prices, foil)
    else:
        create_non_priced_items(card, name, foil)


def create_priced_items(card, name, prices, foil):
    card_prices = prices[name]
    hp_price, mp_price, nm_price, sp_price = get_condition_prices(card_prices)
    hp_buylist, mp_buylist, nm_buylist, sp_buylist = get_buylist_prices(nm_price, sp_price, mp_price, hp_price)
    stock = 0
    nm_item = MagicCardItem(card=card, price=nm_price, buylist=nm_buylist, stock=stock, condition='NM',
                            foil=foil)
    sp_item = MagicCardItem(card=card, price=sp_price, buylist=sp_buylist, stock=stock, condition='SP',
                            foil=foil)
    mp_item = MagicCardItem(card=card, price=mp_price, buylist=mp_buylist, stock=stock, condition='MP',
                            foil=foil)
    hp_item = MagicCardItem(card=card, price=hp_price, buylist=hp_buylist, stock=stock, condition='HP',
                            foil=foil)
    nm_item.save()
    sp_item.save()
    mp_item.save()
    hp_item.save()


def get_buylist_prices(nm_price, sp_price, mp_price, hp_price):
    nm_buylist = nm_price * 0.50
    sp_buylist = sp_price * 0.50
    mp_buylist = mp_price * 0.50
    hp_buylist = hp_price * 0.50
    return hp_buylist, mp_buylist, nm_buylist, sp_buylist


def get_condition_prices(card_prices):
    nm_price = card_prices[0]
    sp_price = card_prices[1]
    mp_price = card_prices[2]
    hp_price = card_prices[3]
    return hp_price, mp_price, nm_price, sp_price


def create_non_priced_items(card, name, foil):
    price = -1
    buylist = -1
    stock = 0
    nm_item = MagicCardItem(card=card, price=price, buylist=buylist, stock=stock, condition='NM',
                            foil=foil)
    sp_item = MagicCardItem(card=card, price=price, buylist=buylist, stock=stock, condition='SP',
                            foil=foil)
    mp_item = MagicCardItem(card=card, price=price, buylist=buylist, stock=stock, condition='MP',
                            foil=foil)
    hp_item = MagicCardItem(card=card, price=price, buylist=buylist, stock=stock, condition='HP',
                            foil=foil)
    nm_item.save()
    sp_item.save()
    mp_item.save()
    hp_item.save()
