from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Fields for categorizing by age group
    AGE_CHOICES = (
        ('5-10', '5-10'),
        ('10-20', '10-20'),
        ('20+', '20+'),
    )
    age_group = models.CharField(max_length=10, choices=AGE_CHOICES)

    # Fields for categorizing by post type
    POST_TYPE_CHOICES = (
        ('Post', 'Post'),
        ('Storytelling', 'Storytelling'),
        ('Poem', 'Poem'),
    )
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES)

    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
