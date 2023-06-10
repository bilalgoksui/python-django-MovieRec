from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
import requests
import json
from django.http import JsonResponse
import json
from .models import Film  
@login_required(login_url='login')
def HomePage(request):
    return render (request,'aihome.html')


def SignupPage(request):
    if request.method=='POST':
        user_name=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')

        if password1!=password2:
            return HttpResponse("Your Password and Conform password are not same")
        
        else:
            user = User.objects.create_user(user_name,email,password1)
            user.save()
            return redirect('login')



    return render (request,'signup.html')

def LoginPage(request):
    if request.method =='POST':
        user_name=request.POST.get('username')
        password=request.POST.get('pass')

        user = authenticate(request,username=user_name,password=password)
        if user is not None :

            login(request,user)
            return redirect('aihome')       
        
        else:
            return HttpResponse(" INVALID USERNAME OR PASSWORD")


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

def suprise_me(request):

    movie_data = {
        "movie_name": "movie_name",
        "emotion_text": "emotion_text",
        "re_suggest":"1",
        "supriseme":1

    }
    json_data = json.dumps(movie_data)

    api_url = "http://127.0.0.1:5655/suggest"  
    response = requests.post(api_url, data=json_data, headers={'Content-Type': 'application/json'})
    response.raise_for_status()  
    
    movie_suggestions = response.json()

    return render(request, 'aihome.html', {'movie_suggestions': movie_suggestions})

def favorites(request):
    films = Film.objects.filter(user=request.user)
    return render(request, 'favorites.html', {'films': films})

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



def delete_favorite(request, film_id):
    film = get_object_or_404(Film, id=film_id, user=request.user)
    if film.user != request.user:
        return redirect('favorites')


    film.delete()
    return redirect('favorites')

def update_favorite(request, film_id):
    film = get_object_or_404(Film, id=film_id, user=request.user)
    if film.user != request.user:
        return redirect('favorites')
    
    if request.method == 'POST':
        film.movie_name = request.POST.get('movie_name')
        film.comment = request.POST.get('comment')
        film.rate = request.POST.get('rate')
        film.save()
        return redirect('favorites')

    return render(request, 'update_favorite.html', {'film': film})


from .models import WatchList

from django.http import JsonResponse
from .models import WatchList

def add_to_watchlist(request, mname):
    # İstediğiniz koşullara göre kullanıcı doğrulaması yapabilirsiniz
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'User is not authenticated'})

    # WatchList nesnesini oluşturup veritabanına kaydediyoruz
    watchlist_item = WatchList(user=request.user, movie_name=mname)
    watchlist_item.save()

    return JsonResponse({'status': 'success', 'message': 'Movie added to watchlist'})



def watchlist_list(request):
    watchlist_items = WatchList.objects.all()
    return render(request, 'watchlist.html', {'watchlist_items': watchlist_items})

# def watchlist_create(request):
#     if request.method == 'POST':
#         form = WatchListForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('watchlist_list')
#     else:
#         form = WatchListForm()
#     return render(request, 'watchlist_form.html', {'form': form})

# def watchlist_edit(request, pk):
#     item = get_object_or_404(WatchList, pk=pk)
#     if request.method == 'POST':
#         form = WatchListForm(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             return redirect('watchlist_list')
#     else:
#         form = WatchListForm(instance=item)
#     return render(request, 'watchlist_form.html', {'form': form})

# def watchlist_delete(request, pk):
#     item = get_object_or_404(WatchList, pk=pk)
#     if request.method == 'POST':
#         item.delete()
#         return redirect('watchlist_list')
#     return render(request, 'watchlist_confirm_delete.html', {'item': item})
