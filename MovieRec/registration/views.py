from gc import get_objects
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
from django.contrib import messages
import requests
import json
from django.http import JsonResponse ,HttpResponse
import json
from .models import Film  ,WatchList
from django.db.models import Q
import re

@login_required(login_url='login')
def HomePage(request):
    return render (request,'aihome.html')

def SignupPage(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        user_email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Your Password and Confirm password do not match')
        elif User.objects.filter(Q(username=user_name) | Q(email=user_email)).exists():
            messages.error(request, 'Username or email already exists')
        elif len(user_name) < 5:
            messages.error(request, 'Username should be at least 5 characters long')
        elif len(password1) < 8:
            messages.error(request, 'Password should be at least 8 characters long')
        elif not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$', password1):
             messages.error(request, 'Password must be 8+ characters with at least one uppercase, one lowercase, and one digit')

        else:
            user = User.objects.create_user(username=user_name, email=user_email, password=password1)
            user.save()
            return redirect('login')

    return render(request, 'signup.html')

def LoginPage(request):
    if request.method =='POST':
        user_name=request.POST.get('username')
        password=request.POST.get('pass')

        user = authenticate(request,username=user_name,password=password)
        if user is not None :

            login(request,user)
            return redirect('aihome')       
        
        else:
            messages.info(request, 'Username or password is incorrect')


    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def AboutPage(request):
        return render (request,'about.html')

@login_required(login_url='login')
def ContactPage(request):
        return render (request,'contact.html')

@login_required(login_url='login')
def get_movie_suggestion(request):
    try:
        movie_name =request.POST.get('movie_name')
        emotion_text = request.POST.get('emotion_text')       
    
        movie_data = {
            "movie_name": movie_name,
            "emotion_text": emotion_text,
            "re_suggest":0,
            "supriseme":0
        }
        json_data = json.dumps(movie_data)
        
        request.session["movie_name"]= movie_name
        request.session["emotion_text"]= emotion_text


        api_url = "http://127.0.0.1:5655/suggest"  
        response = requests.post(api_url, data=json_data, headers={'Content-Type': 'application/json'})
        response.raise_for_status()  
        
        movie_suggestions = response.json()

        return render(request, 'aihome.html', {'movie_suggestions': movie_suggestions})
    
    except requests.exceptions.RequestException:
        return HttpResponse('Service is currently unavailable')

@login_required(login_url='login')
def get_new_suggestion(request):

    movie_name = request.session.get('movie_name')
    emotion_text = request.session.get('emotion_text')

    movie_data = {
        "movie_name": movie_name,
        "emotion_text": emotion_text,
        "re_suggest":1,
        "supriseme":0


    }
    json_data = json.dumps(movie_data)

    api_url = "http://127.0.0.1:5655/suggest"  
    response = requests.post(api_url, data=json_data, headers={'Content-Type': 'application/json'})
    response.raise_for_status()  
    
    movie_suggestions = response.json()

    return render(request, 'aihome.html', {'movie_suggestions': movie_suggestions})


@login_required(login_url='login')
def suprise_me(request):
    try:
        movie_data = {
            "movie_name": "movie_name",
            "emotion_text": "emotion_text",
            "re_suggest": "1",
            "supriseme": 1
        }
        json_data = json.dumps(movie_data)

        api_url = "http://127.0.0.1:5655/suggest"
        response = requests.post(api_url, data=json_data, headers={'Content-Type': 'application/json'})
        response.raise_for_status()

        movie_suggestions = response.json()

        return render(request, 'aihome.html', {'movie_suggestions': movie_suggestions})

    except requests.exceptions.RequestException:
        return HttpResponse('Service is currently unavailable')


@login_required(login_url='login')
def favorites(request):
    films = Film.objects.filter(user=request.user)
    return render(request, 'favorites.html', {'films': films})

@login_required(login_url='login')
def save_comment(request):
    if request.method == 'POST':
        movie_name = request.POST.get('movie_name')
        comment = request.POST.get('comment')
        rate = request.POST.get('rate')

        # Retrieve the logged-in user's information
        user = request.user

        # Create and save the Film object to the database
        film = Film(user=user, movie_name=movie_name, comment=comment, rate=rate)
        film.save()

    return redirect('favorites')

@login_required(login_url='login')
def delete_favorite(request, film_id):
    try:
        film = Film.objects.get(id=film_id, user=request.user)
    except Film.DoesNotExist:
        return redirect('favorites')


    film.delete()
    return redirect('favorites')

@login_required(login_url='login')
def update_favorite(request, film_id):
    try:
        film = Film.objects.get(id=film_id, user=request.user)
    except Film.DoesNotExist:
        return redirect('favorites')
        
    if request.method == 'POST':
        film.movie_name = request.POST.get('movie_name')
        film.comment = request.POST.get('comment')
        film.rate = request.POST.get('rate')
        film.save()
        return redirect('favorites')

    return render(request, 'update_favorite.html', {'film': film})

@login_required(login_url='login')
def add_to_watchlist(request, mname):
    # İstediğiniz koşullara göre kullanıcı doğrulaması yapabilirsiniz
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'User is not authenticated'})

    # WatchList nesnesini oluşturup veritabanına kaydediyoruz
    watchlist_item = WatchList(user=request.user, movie_name=mname)
    watchlist_item.save()

    return JsonResponse({'status': 'success', 'message': 'Movie added to watchlist'})

@login_required(login_url='login')
def watchlist_list(request):
    watchlist_items = WatchList.objects.filter(user=request.user)
    return render(request, 'watchlist.html', {'watchlist_items': watchlist_items})

@login_required(login_url='login')
def update_watched_status(request, item_id):
    try:
        watchlist_item = WatchList.objects.get(id=item_id)
        watchlist_item.is_watched = not watchlist_item.is_watched
        watchlist_item.save()
        return JsonResponse({'status': 'success', 'message': 'Watched status updated'})
    except WatchList.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Watchlist item not found'})

@login_required(login_url='login')
def delete_item(request, item_id):
    try:
        watchlist_item = WatchList.objects.get(id=item_id)
        watchlist_item.delete()
        return JsonResponse({'status': 'success', 'message': 'Item deleted'})
    except WatchList.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Watchlist item not found'})