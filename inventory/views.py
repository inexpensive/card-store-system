import json
from pprint import pprint

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views import generic

from inventory.templatetags.card_filters import replace_symbols
from .models import Card, Set


class IndexView(generic.ListView):
    template_name = 'inventory/index.html'
    context_object_name = 'set_list'

    def get_queryset(self):
        return Set.objects.order_by('-release_date')


class SetView(generic.ListView):
    model = Card
    template_name = 'inventory/cardlist.html'

    def get_queryset(self):
        return Card.objects


class SearchView(generic.ListView):
    model = Card
    template_name = 'inventory/cardlist.html'

    def get_queryset(self):
        return Card.objects


class CardDetailsView(generic.DetailView):
    model = Card
    template_name = 'inventory/carddetails.html'


def index(request):
    set_list = Set.objects.order_by('-release_date')
    template = loader.get_template('inventory/index.html')
    context = {
        'set_list': set_list,
    }
    return render(request, 'inventory/index.html', context)


def cardset(request, set_id):
    card_list = get_list_or_404(Card.objects.order_by('name'), set=set_id, foil=False, condition='NM')
    return render(request, 'inventory/cardlist.html', {'card_list': card_list})


def search(request):
    if request.method == 'GET':
        query = request.GET.get('card_search_box', None)
        vector = SearchVector('name', weight='A') + \
            SearchVector('super_types_text', 'types_text', 'sub_types_text', weight='B') + \
            SearchVector('rules_text', weight='C') + \
            SearchVector('color_text', 'power', 'toughness', 'artist', 'flavor_text', weight='D')
        search_query = SearchQuery(query)
        card_list = Card.objects.annotate(
            search=vector,
            rank=SearchRank(vector, search_query)
        ).filter(search=query, foil=False, condition='NM', ).order_by('-rank', 'name')
        return render(request, 'inventory/cardlist.html', {'card_list': card_list})


def autocomplete(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        cards = Card.objects.filter(name__icontains=q, condition='NM', foil=False).order_by('name').distinct(
            'name')[:10]
        results = []
        for card in cards:
            card_json = {
                'label': card.name,
                'value': card.name,
                'desc': replace_symbols(card.rules_text),
                'id': card.id,
                'image': str(card.image),
            }
            results.append(card_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def card_details(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    return render(request, 'inventory/carddetails.html', {'card': card})
