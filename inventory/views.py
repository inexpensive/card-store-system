import json
from pprint import pprint

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
    paginator = Paginator(card_list, 25)
    page = request.GET.get('page')
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)
    return render(request, 'inventory/cardlist.html', {'card_list': cards})


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
        ).filter(card_search=query, foil=False, condition='NM', ).order_by('-rank', 'name')
        print(card_list.query)
        paginator = Paginator(card_list, 25)
        page = request.GET.get('page')
        try:
            cards = paginator.page(page)
        except PageNotAnInteger:
            cards = paginator.page(1)
        except EmptyPage:
            cards = paginator.page(paginator.num_pages)
        return render(request, 'inventory/search.html', {'card_list': cards, 'query': query})


def autocomplete(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        cards = Card.objects\
                    .filter(name__icontains=q, condition='NM', foil=False)\
                    .exclude(image='/images/None/no_art.jpg')\
                    .order_by('name', 'set__release_date').distinct('name')[:10]
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


def pricing(request):
    return render(request, 'inventory/pricing.html')
