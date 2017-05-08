from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /inv/5/
    url(r'^set/(?P<set_id>[0-9]+)/$', views.cardset, name='cardset'),
    # ex: /inv/card/5
    url(r'^card/(?P<card_id>[0-9]+)/$', views.card_details, name='card_details'),
    # ex: /inv/search/card_search_box=island
    url(r'^search/.*$', views.search, name='search'),
    # ex: /inv/autocomplete/
    url(r'^autocomplete/.*$', views.autocomplete, name='autocomplete'),
    # ex: /inv/pricing/
    url(r'^pricing/.*$', views.pricing_ajax),
]
