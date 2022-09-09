from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import*
from .filters import PostFilter
from .forms import PostForm, ArticlesPostForm


class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostSearch(ListView):
    model = Post
    ordering = ['title']
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
       queryset = super().get_queryset()
       self.filterset = PostFilter(self.request.GET, queryset)
       return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def create_post(request):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/posts/')

        form = PostForm()
        return render(request, 'news_create.html', {'form': form})

    def form_valid(self, form):
        new = form.save(commit=False)
        new.categories = 'NW'
        return super().form_valid(form)


class ArticlesPostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_create.html'

    def create_articles(request):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/posts/')

        form = PostForm()
        return render(request, 'articles_create.html', {'form': form})

    def form_valid(self, form):
        articles = form.save(commit=False)
        articles.categories = 'AR'
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    context_object_name = 'new_edit'


class ArticlesPostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'
    context_object_name = 'articles_edit'


class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class ArticlesPostDelete(DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('post_list')





















