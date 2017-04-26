from django.core.urlresolvers import reverse
from django.template import loader
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic
from .models import Card


class IndexView(generic.ListView):
    template_name = 'inventory/index.html'
    context_object_name = 'card_list'

    def get_queryset(self):
        return Card.objects.order_by('multiverse_id', 'foil')


class DetailView(generic.DetailView):
    model = Card
    template_name = 'inventory/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Card.objects


class ResultsView(generic.DetailView):
    model = Card
    template_name = 'inventory/results.html'


def index(request):
    card_list = Card.objects.filter(foil=False).order_by('name')
    template = loader.get_template('inventory/index.html')
    context = {
        'card_list' : card_list,
    }
    return render(request, 'inventory/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Card, pk=question_id)
    return render(request, 'inventory/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Card, pk=question_id)
    return render(request, 'inventory/results.html', {'question': question})

