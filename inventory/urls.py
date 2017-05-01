from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /inv/5/
    url(r'^(?P<set_id>[0-9]+)/$', views.cardset, name='cardset'),
    # ex: /inv/5/results
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /inv/search/query
    url(r'^search/(?P<query>.+)/$', views.search, name='search'),
]
