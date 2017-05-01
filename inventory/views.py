from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from django.template import loader
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views import generic
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


class ResultsView(generic.DetailView):
    model = Card
    template_name = 'inventory/results.html'


def index(request):
    set_list = Set.objects.order_by('-release_date')
    template = loader.get_template('inventory/index.html')
    context = {
        'set_list': set_list,
    }
    return render(request, 'inventory/index.html', context)


def cardset(request, set_id):
    card_list = get_list_or_404(Card.objects.order_by('multiverse_id'), set=set_id, foil=False, condition='NM')
    return render(request, 'inventory/cardlist.html', {'card_list': card_list})


def search(request, query):
    print(query)
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


def results(request, question_id):
    question = get_object_or_404(Card, pk=question_id)
    return render(request, 'inventory/results.html', {'question': question})
