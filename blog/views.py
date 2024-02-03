'''
Представления для задачи Блог
'''

from django.views.generic import CreateView, DeleteView, ListView, DetailView, UpdateView
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify

from blog.forms import BlogForm
from blog.models import Blog


class BlogListView(ListView):
    model = Blog
    extra_context = {
        'title': 'Список статей',
    }


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')
    extra_context = {
        'title': 'Создание статьи',
    }


class BlogDetailView(DetailView):
    model = Blog
    extra_context = {
        'title': 'Подробности статьи',
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_views += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')
    extra_context = {
        'title': 'Обновить статью',
    }

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')
    extra_context = {
        'title': 'Удаление статьи',
    }
