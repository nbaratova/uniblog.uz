import openai
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from .models import Post
from .forms import CategoryFilterForm, PostTypeFilterForm, AgeGroupFilterForm


openai.api_key = ''

def transform_content(original_content, age_group='5-10'):
    # Define a prompt for GPT-3 based on the age group

    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": f"Transform this content into storytelling for {age_group}:\n\n{original_content}",
            },
        ],
        temperature=0,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return gpt_response["choices"][0]["message"]["content"]


def transform_content_to_poem(original_content, age_group='5-10'):
    # Define a prompt for GPT-3 based on the age group

    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": f"Transform this content into 12 rows poem for {age_group}:\n\n{original_content}",
            },
        ],
        temperature=0,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return gpt_response["choices"][0]["message"]["content"]


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

    def form_valid(self, form):
        # Get the original content from the form
        original_content = form.cleaned_data['content']

        # Transform the content into storytelling for all age groups
        transformed_content_5_10_storytelling = transform_content(original_content, age_group='5-10')
        transformed_content_10_20_storytelling = transform_content(original_content, age_group='10-20')
        transformed_content_20_plus_storytelling = transform_content(original_content, age_group='20+')

        # Transform the content into poem for all age groups
        transformed_content_5_10_poem = transform_content_to_poem(original_content, age_group='5-10')
        transformed_content_10_20_poem = transform_content_to_poem(original_content, age_group='10-20')
        transformed_content_20_plus_poem = transform_content_to_poem(original_content, age_group='20+')

        # Create the original post
        original_post = form.save(commit=False)
        original_post.save()

        # Create and save posts for age group 5-10
        post_5_10_storytelling = Post(
            title=form.cleaned_data['title'],
            content=transformed_content_5_10_storytelling,
            age_group='5-10',
            post_type='Storytelling',
            image=form.cleaned_data['image'],
            category=form.cleaned_data['category'],
        )
        post_5_10_storytelling.save()

        post_5_10_poem = Post(
            title=form.cleaned_data['title'],
            content=transformed_content_5_10_poem,
            age_group='5-10',
            post_type='Poem',
            image=form.cleaned_data['image'],
            category=form.cleaned_data['category'],
        )
        post_5_10_poem.save()

        # Create and save posts for age group 10-20
        post_10_20_storytelling = Post(
            title=form.cleaned_data['title'],
            content=transformed_content_10_20_storytelling,
            age_group='10-20',
            post_type='Storytelling',
            image=form.cleaned_data['image'],
            category=form.cleaned_data['category'],
        )
        post_10_20_storytelling.save()

        post_10_20_poem = Post(
            title=form.cleaned_data['title'],
            content=transformed_content_10_20_poem,
            age_group='10-20',
            post_type='Poem',
            image=form.cleaned_data['image'],
            category=form.cleaned_data['category'],
        )
        post_10_20_poem.save()

        # Create and save posts for age group 20+
        post_20_plus_storytelling = Post(
            title=form.cleaned_data['title'],
            content=transformed_content_20_plus_storytelling,
            age_group='20+',
            post_type='Storytelling',
            image=form.cleaned_data['image'],
            category=form.cleaned_data['category'],
        )
        post_20_plus_storytelling.save()

        post_20_plus_poem = Post(
            title=form.cleaned_data['title'],
            content=transformed_content_20_plus_poem,
            age_group='20+',
            post_type='Poem',
            image=form.cleaned_data['image'],
            category=form.cleaned_data['category'],
        )
        post_20_plus_poem.save()

        return super().form_valid(form)


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
