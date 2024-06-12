from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Movie, MovieList
import requests
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseForbidden

OMDB_API_KEY = 'f45324e4'

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username or password is not correct')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def home(request):
    movie_lists = MovieList.objects.filter(user=request.user)
    return render(request, 'movie/home.html', {'movie_lists': movie_lists})

@login_required
def search(request):
    query = request.GET.get('q')
    movies = []
    if query:
        response = requests.get(f'http://www.omdbapi.com/?s={query}&apikey={OMDB_API_KEY}')
        data = response.json()
        if data['Response'] == 'True':
            movies = data['Search']
    return render(request, 'movie/search.html', {'movies': movies})

@login_required
def movie_detail(request, imdb_id):
    response = requests.get(f'http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}')
    movie_data = response.json()
    movie, created = Movie.objects.get_or_create(
        imdb_id=imdb_id,
        defaults={
            'title': movie_data['Title'],
            'description': movie_data['Plot'],
            'release_date': movie_data['Released'],
            'poster_url': movie_data['Poster'],
        }
    )
    return render(request, 'movie/movie_detail.html', {'movie': movie})

@login_required
def create_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        is_public = request.POST.get('is_public') == 'on'
        movie_list = MovieList.objects.create(user=request.user, name=name, is_public=is_public)
        return redirect('home')
    return render(request, 'movie/create_list.html')

@login_required
def add_to_list(request, imdb_id):
    movie = Movie.objects.get(imdb_id=imdb_id)
    lists = MovieList.objects.filter(user=request.user)
    if request.method == 'POST':
        list_id = request.POST.get('list_id')
        movie_list = MovieList.objects.get(id=list_id)
        movie_list.movies.add(movie)
        return redirect('home')
    return render(request, 'movie/add_to_list.html', {'movie': movie, 'lists': lists})

@login_required
def view_list(request, list_id):
    movie_list = MovieList.objects.get(id=list_id)
    return render(request, 'movie/view_list.html', {'movie_list': movie_list})

@login_required
def delete_list(request, list_id):
    movie_list = MovieList.objects.get(id=list_id)
    movie_list.delete()
    return redirect('home')

@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    movie_lists = MovieList.objects.filter(movies=movie)
    user_is_owner = any(request.user == movie_list.user for movie_list in movie_lists)

    if user_is_owner:
        for movie_list in movie_lists:
            movie_list.movies.remove(movie)
        if not MovieList.objects.filter(movies=movie).exists():
            movie.delete()
        return redirect('home')  
    else:
        return HttpResponseForbidden("You do not have permission to delete this movie.")