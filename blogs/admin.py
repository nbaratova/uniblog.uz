from django.contrib import admin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'age_group', 'post_type', 'category')
    list_filter = ('age_group', 'post_type', 'category')
    search_fields = ('title', 'content')
