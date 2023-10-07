from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


class PostList(ListView):
    model = Post
    template_name = 'blogs/post_list.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'blogs/post_detail.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    model = Post
    template_name = 'blogs/post_form.html'
    fields = ['title', 'content', 'age_group', 'post_type', 'category']
    success_url = reverse_lazy('blogs:post_list')


class PostUpdate(UpdateView):
    model = Post
    template_name = 'blogs/post_form.html'
    fields = ['title', 'content', 'age_group', 'post_type', 'category']
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('blogs:post_detail', kwargs={'pk': self.object.pk})


class PostDelete(DeleteView):
    model = Post
    template_name = 'blogs/post_confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blogs:post_list')


def home(request):
    return render(request, 'blogs/home.html')
