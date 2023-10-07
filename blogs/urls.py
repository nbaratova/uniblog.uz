from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.home, name='home'),
    path('posts', views.PostList.as_view(), name='post_list'),
    path('create/', views.PostCreate.as_view(), name='post_create'),
    path('<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('<int:pk>/update/', views.PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),
]
