from django.conf.urls import url
from tutorial.views import TpostLV, TpostDV

urlpatterns = [
    url(r'^$', TpostLV.as_view(), name='index'),
    url(r'^post/$', TpostLV.as_view(), name='post_list'),
    url(r'^post/(?P<slug>[-\w]+)/$', TpostDV.as_view(), name='post_detail'),

]
