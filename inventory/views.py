import json

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.views import generic

from inventory.templatetags.card_filters import replace_symbols
from .models import MagicCard, MagicSet
from .forms import UserForm, ProfileForm


class IndexView(generic.ListView):
    template_name = 'inventory/index.html'
    context_object_name = 'set_list'

    def get_queryset(self):
        return MagicSet.objects.order_by('-release_date')


class MagicSetView(generic.ListView):
    model = MagicCard
    template_name = 'inventory/cardlist.html'

    def get_queryset(self):
        return MagicCard.objects


class SearchView(generic.ListView):
    model = MagicCard
    template_name = 'inventory/cardlist.html'

    def get_queryset(self):
        return MagicCard.objects


class MagicCardDetailsView(generic.DetailView):
    model = MagicCard
    template_name = 'inventory/carddetails.html'


def index(request):
    set_list = MagicSet.objects.order_by('-release_date')
    template = loader.get_template('inventory/index.html')
    context = {
        'set_list': set_list,
    }
    return render(request, 'inventory/index.html', context)


def cardset(request, set_id):
    card_list = get_list_or_404(MagicCard.objects.order_by('name'), set=set_id)
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
        card_list = MagicCard.objects.annotate(
            search=vector,
            rank=SearchRank(vector, search_query)
        ).filter(card_search=query).order_by('-rank', 'name')
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
        cards = MagicCard.objects \
            .filter(name__icontains=q) \
            .exclude(image='/images/None/no_art.jpg') \
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
    card = get_object_or_404(MagicCard, pk=card_id)
    return render(request, 'inventory/carddetails.html', {'card': card})


def pricing(request):
    if request.user.groups.filter(name='Employees').exists():
        return render(request, 'inventory/pricing.html')
    else:
        return HttpResponseNotFound()


def pricing_ajax(request):
    if request.is_ajax():
        q = request.GET.get('name', '')
        cards = MagicCard.objects.filter(name=q).order_by('-set__release_date', 'set__name')[:64]
        condition_order = {
            'NM': 1,
            'SP': 2,
            'MP': 3,
            'HP': 4,
        }
        cards = sorted(cards, key=lambda x: condition_order[x.condition])
        results = []
        for card in cards:
            card_json = {
                'name': card.name,
                'set': card.set.name,
                'condition': card.condition,
                'price': card.price,
            }
            results.append(card_json)
        data = json.dumps(results)
    else:
        data = 'nope'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user_profile = profile_form.save(commit=False)
            user_profile.user = user
            user_profile.save()
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/inv/')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'inventory/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
