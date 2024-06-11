# movies/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('movie/<str:imdb_id>/', views.movie_detail, name='movie_detail'),
    path('create_list/', views.create_list, name='create_list'),
    path('add_to_list/<str:imdb_id>/', views.add_to_list, name='add_to_list'),
    path('list/<int:list_id>/', views.view_list, name='view_list'),
]
