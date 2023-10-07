from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from .models import Post
from .forms import CategoryFilterForm, PostTypeFilterForm, AgeGroupFilterForm


class PostList(ListView):
    model = Post
    template_name = 'blogs/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()

        selected_category = self.request.GET.get('category')
        selected_post_type = self.request.GET.get('post_type')
        selected_age_group = self.request.GET.get('age_group')

        if selected_category:
            queryset = queryset.filter(category=selected_category)

        if selected_post_type:
            queryset = queryset.filter(post_type=selected_post_type)

        if selected_age_group:
            queryset = queryset.filter(age_group=selected_age_group)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_filter_form'] = CategoryFilterForm(self.request.GET)
        context['post_type_filter_form'] = PostTypeFilterForm(self.request.GET)
        context['age_group_filter_form'] = AgeGroupFilterForm(self.request.GET)
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'blogs/post_detail.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    model = Post
    template_name = 'blogs/post_form.html'
    fields = ['title', 'content', 'image', 'category']
    success_url = reverse_lazy('blogs:post_list')


class PostUpdate(UpdateView):
    model = Post
    template_name = 'blogs/post_form.html'
    fields = ['title', 'content', 'image', 'category']
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


def blog_post_search(request):
    query = request.GET.get('q')
    results = []

    if query:
        # Perform a case-insensitive search on the 'title' field
        results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))

    return render(request, 'blogs/post_list.html', {'posts': results, 'query': query})
