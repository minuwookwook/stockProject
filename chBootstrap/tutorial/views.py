from django.shortcuts import render
from django.views.generic import ListView, DetailView

from tutorial.models import Tpost

# Create your views here.


#-- ListView
class TpostLV(ListView):
    model = Tpost
    template_name = 'tutorial/tpost_all.html'
    context_object_name = 'posts'
    paginate_by = 5

class TpostDV(DetailView):
    model = Tpost
