from django.core.urlresolvers import reverse
from django.template import loader
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.utils import timezone
from django.views import generic
from .models import Card, Set


class IndexView(generic.ListView):
    template_name = 'inventory/index.html'
    context_object_name = 'set_list'

    def get_queryset(self):
        return Set.objects.order_by('-release_date')


class SetView(generic.DetailView):
    model = Card
    template_name = 'inventory/set.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Card.objects


class ResultsView(generic.DetailView):
    model = Card
    template_name = 'inventory/results.html'


def index(request):
    set_list = Set.objects.order_by('-release_date')
    template = loader.get_template('inventory/index.html')
    context = {
        'set_list' : set_list,
    }
    return render(request, 'inventory/index.html', context)


def cardset(request, set_id):
    card_list = get_list_or_404(Card.objects.order_by('multiverse_id'), set=set_id, foil=False, condition='NM')
    return render(request, 'inventory/set.html', {'card_list': card_list})


def results(request, question_id):
    question = get_object_or_404(Card, pk=question_id)
    return render(request, 'inventory/results.html', {'question': question})

