from django import urls
from django.urls import path

from .views import *

app_name = "blog"

urlpatterns = [
    path('blogs/', TechStackListView.as_view(), name='tech_list'),
    path('blogs/<slug:slug>/', BlogListView.as_view(), name='blog_list'),
    path('blogs/<slug:slug>/<str:str>/', BlogAPIView.as_view(), name='blog_api'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
    path('like/', LikeView, name='blog_likes'),
    path('tech/trends/', TechStackListView.as_view(), name='trend_list'),
]



