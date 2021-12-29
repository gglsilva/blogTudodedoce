from django.urls import path
from django.urls.resolvers import URLPattern
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
]
