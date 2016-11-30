from django.conf.urls import url
from stocks.views import *


urlpatterns = [
    url(r'^$',calculate, name='index'),
    url(r'^cal/', calculate, name='calculate'),
]
