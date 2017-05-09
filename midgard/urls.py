"""midgard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

import inventory.views
import common.util.SetParser
import common.util.CardParser

urlpatterns = [
    url(r'^inv/', include('inventory.urls', namespace='inventory')),
    url(r'^login', auth_views.login, name='login'),
    url(r'^logout', auth_views.logout, {'next_page': '/inv/'}, name='logout'),
    url(r'^pricing/', inventory.views.pricing),
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', inventory.views.signup, name='signup'),
    url(r'^parse_all_sets$', common.util.SetParser.parse_all_sets),
    url(r'^parse_all_cards$', common.util.CardParser.parse_all_cards),
]
