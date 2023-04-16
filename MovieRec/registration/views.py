from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
import requests
import json
from django.http import JsonResponse
import json

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
        "re_suggest":1

    }
    json_data = json.dumps(movie_data)

    api_url = "http://127.0.0.1:5655/suggest"  
    response = requests.post(api_url, data=json_data, headers={'Content-Type': 'application/json'})
    response.raise_for_status()  
    
    movie_suggestions = response.json()

    return render(request, 'aihome.html', {'movie_suggestions': movie_suggestions})