from lib2to3.pytree import generate_matches
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
import json
from django.http import JsonResponse ,HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.signing import Signer
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes ,force_str
from .models import Film  ,WatchList , Feedback
from django.db.models import Q
import re
from django.contrib.auth.hashers import  check_password
from django.core.signing import Signer, BadSignature, SignatureExpired
from django.http import HttpResponseBadRequest
from django.urls import reverse


def hub(request):
    
    return render (request,'hub.html')

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
            user.is_active = False
            user.save()

            # Doğrulama linki oluşturma
            signer = Signer()
            user_id = urlsafe_base64_encode(force_bytes(user.pk))
            token = signer.sign(user_id)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            mail_message = render_to_string('activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'token': token,
            })
            send_mail(mail_subject, mail_message, 'settings.EMAIL_HOST_USER', [user_email], fail_silently=False)
            
            return redirect('login')

    return render(request, 'signup.html')

def LoginPage(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('pass')

        user = authenticate(request, username=user_name, password=password, backend='django.contrib.auth.backends.ModelBackend')
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('aihome')
            else:
                messages.info(request, 'Inactive account. Please check your email.')
        else:
            messages.info(request, 'Username or password is incorrect')

    return render(request, 'login.html')

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


# def save_feedback(request):
#     if request.method == 'POST':
#         liked = request.POST.get('liked')
#         movie_title = request.POST.get('movie_title')
#         imdb_id = request.POST.get('imdb_id')
#         genres = request.POST.get('genres')
#         genre_matches= request.POST.get('genre_matches')
#         csrf_token = request.POST.get('csrfmiddlewaretoken')  # 'csrfmiddlewaretoken' parametresini al
        
#         print('movie_title:', movie_title)
#         print('imdb_id:', imdb_id)
#         print('genres:', genres)
#         print('genre_matches:', genre_matches)
        
#         print('liked:', liked)
#         print('csrf_token:', csrf_token)

#         user = request.user
#         smilar_movie = "DENEME"
#         mood_text = "DENEME"
#         movie_name = "DENEME"
#         imdb_title = "DENEME"
#         genres ="DENEME"
#         genres_match = 1 
#         feedback = True
#         feedback = Feedback(user=user, smilar_movie=smilar_movie, mood_text=mood_text, genres=genres , genres_match=genres_match, movie_name=movie_name, feedback=feedback)
#         feedback.save()

#         return JsonResponse({'status': 'success', 'message': 'Feedback saved successfully'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request'})

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
    
@login_required
def profile(request):
    if request.method == 'POST':
        username_ = request.POST.get('username')
        email_ = request.POST.get('email')
        user = request.user

        # Update user object with new data
        user.username = username_
        user.email = email_
        user.save()

    user = request.user
    return render(request, 'profile.html', {'user': user})

def delete_profile(request):
    user = request.user
    user.delete()
    return redirect('login')

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        oldpassword = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')
        renewpassword = request.POST.get('renewpassword')

        user = request.user  # Geçerli kullanıcıyı al

        if check_password(oldpassword, user.password):  # Eski şifre eşleşiyor mu kontrol et
            if newpassword == renewpassword:  # Yeni şifre ve yeniden girilen şifre eşleşiyor mu kontrol et
                user.set_password(newpassword)  # Kullanıcının şifresini güncelle
                user.save()
                user = authenticate(request, username=request.user.username, password=newpassword)
                login(request, user)
                return redirect('profile')
            else:
                return HttpResponse('Yeni şifreler eşleşmiyor.')
        else:
            return HttpResponse('Eski şifre yanlış.')

    return render(request, 'changepassword.html')

def activate_account(request, token):
    signer = Signer()
    try:
        user_id = signer.unsign(token)
        user_id = force_str(urlsafe_base64_decode(user_id))
        user = User.objects.get(pk=user_id)
        user.is_active = True
        user.save()
        return HttpResponse('Your account has been activated successfully.')
    except (BadSignature, SignatureExpired, User.DoesNotExist):
        return HttpResponseBadRequest('Invalid activation link.')
    
def forgot_password(request):
    if request.method == 'POST':
        email_ = request.POST.get("email")
        if email_:
            signer = Signer()
            user = User.objects.get(email=email_)
            user_id = urlsafe_base64_encode(force_bytes(user.pk))
            token = signer.sign(user_id)
            current_site = get_current_site(request)
            reset_url = reverse('reset_password', kwargs={'user_id': user_id, 'token': token, 'user_email': email_})
            reset_url = request.build_absolute_uri(reset_url)
            mail_subject = 'Reset your password'
            mail_message = f"Click the following link to reset your password: {reset_url}"
            send_mail(mail_subject, mail_message, 'settings.EMAIL_HOST_USER', [email_], fail_silently=False)
    return render(request, 'forgotpassword.html')

def reset_password(request, user_id, token, user_email):
    try:
        signer = Signer()
        user_id = urlsafe_base64_decode(user_id)
        token = signer.unsign(token)
        user = User.objects.get(pk=user_id)
        if user.email == user_email:
            if request.method == 'POST':
                new_password = request.POST.get("new_password")
                confirm_password = request.POST.get("confirm_password")
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Şifreniz başarıyla değiştirildi.')
                    return redirect('login')  # Yönlendirilecek sayfa
                else:
                    messages.error(request, 'Yeni şifreler eşleşmiyor.')
                    return redirect('reset_password', user_id=user_id, token=token, user_email=user_email)
            return render(request, 'reset_password.html', {'user_id': user_id, 'token': token, 'user_email': user_email})
    except (BadSignature, SignatureExpired, User.DoesNotExist):
        messages.error(request, 'Geçersiz veya süresi dolmuş bir şifre sıfırlama talebi.')
        return redirect('forgot_password')  # Yönlendirilecek sayfa
    
 