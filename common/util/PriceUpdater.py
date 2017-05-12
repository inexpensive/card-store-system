from common.util.PriceFetcher import PriceFetcher
from inventory.models import MagicSet, MagicCardItem


def update_all_prices(request):
    price_fetcher = PriceFetcher()
    sets = MagicSet.objects.all()
    non_foil_set_prices = {}
    foil_set_prices = {}
    for set_ in sets:
        set_code = set_.code
        non_foil_set_prices[set_code] = price_fetcher.get_set_prices(set_code)
        foil_set_prices[set_code] = price_fetcher.get_set_prices(set_code, foil=True)
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


