"""
URL configuration for MovieRec project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from registration import views
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', views.HomePage,name='aihome'),

    path('home/', views.HomePage,name='aihome'),
    path('login/', views.LoginPage,name='login'),
    path('signup/', views.SignupPage,name='signup'),
    path('logout/', views.LogoutPage,name='logout'),
    path('about/', views.AboutPage,name='about'),
    path('contact/', views.ContactPage,name='contact'),
    path('suggest/', views.get_movie_suggestion,name='suggest'),
    path('suggestnew/', views.get_new_suggestion,name='newsuggest'),
    path('supriseme/', views.suprise_me,name='supriseme'),

    path('favorites/', views.favorites, name='favorites'),

    path('save_comment/', views.save_comment, name='save_comment'),
    path('favorites/delete/<int:film_id>/', views.delete_favorite, name='delete_favorite'),
    path('favorites/update/<int:film_id>/', views.update_favorite, name='update_favorite'),


    path('add_to_watchlist/<str:mname>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/', views.watchlist_list, name='watchlist'),
    path('update_watched_status/<int:item_id>/', views.update_watched_status, name='update_watched_status'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
   
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
