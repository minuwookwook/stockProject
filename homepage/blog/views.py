from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from blog.models import Post
from tagging.models import Tag, TaggedItem
from tagging.views import TaggedObjectList

from django.views.generic.edit import FormView
from blog.forms import PostSearchForm
from django.db.models import Q
from django.shortcuts import render
from blog.forms import Cal

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from mysite.views import LoginRequiredMixin




class CView(TemplateView) :
    template_name = 'blog/calculate.html'
    def calculate(request) :
     result=""
     temp = "hello"

     if request.method == "GET":
         _numform = Cal()
     elif request.method == "POST":
         _numform = Cal(request.POST)
         if _numform.is_valid():
             number1 = _numform.cleanded_data['number1']
             number2 = _numform.cleanded_data['number2']
             result = number1 + number2
     return render_to_response('blog/calculate.html', {'temp': temp})






# Create your views here.

#--- TemplateView
class TagTV(TemplateView) :
    template_name = 'tagging/tagging_cloud.html'

#--- ListView
class PostLV(ListView) :
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'
    paginate_by = 5

class PostTOL(TaggedObjectList) :
    model = Post
    template_name = 'tagging/tagging_post_list.html'

#--- DetailView
class PostDV(DetailView) :
    model = Post

#--- ArchiveView
class PostAV(ArchiveIndexView) :
    model = Post
    date_field = 'modify_date'

class PostYAV(YearArchiveView) :
    model = Post
    date_field = 'modify_date'
    make_object_list = True

class PostMAV(MonthArchiveView) :
    model = Post
    date_field = 'modify_date'

class PostDAV(DayArchiveView) :
    model = Post
    date_field = 'modify_date'

class PostTAV(TodayArchiveView) :
    model = Post
    date_field = 'modify_date'

#--- FormView
class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name = 'blog/post_search.html'

    def form_valid(self, form) :
        schWord = '%s' % self.request.POST['search_word']
        post_list = Post.objects.filter(Q(title__icontains=schWord) | Q(description__icontains=schWord) | Q(content__icontains=schWord)).distinct()

        context = {}
        context['form'] = form
        context['search_term'] = schWord
        context['object_list'] = post_list

        return render(self.request, self.template_name, context)

#--- Bootstrap Search Result
class BstrapSearchLV(ListView) :
    template_name = 'blog/post_bstrap_search.html'

    def get_queryset(self):
        schWord = '%s' % self.request.GET['search']
        post_list = Post.objects.filter(Q(title__icontains=schWord) | Q(description__icontains=schWord) | Q(content__icontains=schWord)).distinct()
        self.search_term = schWord
        self.count = post_list.count()
        return post_list

    def get_context_data(self, **kwargs):
        context = super(BstrapSearchLV, self).get_context_data(**kwargs)
        context['search_term'] = self.search_term
        context['search_count'] = self.count
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tag']
    initial = {'slug': 'auto-filling-do-not-input'}
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostChangeLV(LoginRequiredMixin, ListView):
    template_name = 'blog/post_change_list.html'

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)

class PostUpdateView(LoginRequiredMixin, UpdateView) :
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tag']
    success_url = reverse_lazy('blog:index')

class PostDeleteView(LoginRequiredMixin, DeleteView) :
    model = Post
    success_url = reverse_lazy('blog:index')
