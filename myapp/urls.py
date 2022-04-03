from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recommend_movie', views.recommendMovie, name='recommend_movie'),
]
