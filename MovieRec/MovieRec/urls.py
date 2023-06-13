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
from django.utils.encoding import force_str

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', views.HomePage,name='aihome'),
    
    path('hub/', views.hub,name='hub'),

    path('home/', views.HomePage,name='aihome'),
    path('login/', views.LoginPage,name='login'),
    path('signup/', views.SignupPage,name='signup'),
    path('logout/', views.LogoutPage,name='logout'),
    path('about/', views.AboutPage,name='about'),
    path('contact/', views.ContactPage,name='contact'),
    path('suggest/', views.get_movie_suggestion,name='suggest'),
    path('supriseme/', views.suprise_me,name='supriseme'),

    path('favorites/', views.favorites, name='favorites'),

    path('save_comment/', views.save_comment, name='save_comment'),
    path('favorites/delete/<int:film_id>/', views.delete_favorite, name='delete_favorite'),
    path('favorites/update/<int:film_id>/', views.update_favorite, name='update_favorite'),


    path('add_to_watchlist/<str:mname>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/', views.watchlist_list, name='watchlist'),
    path('update_watched_status/<int:item_id>/', views.update_watched_status, name='update_watched_status'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),

    path('profile/', views.profile, name='profile'),
    # path('profile/update', views.update_profile, name='update_profile'),
    path('profile/changepassword/', views.change_password, name='change_password'),
    path('deleteprofile/', views.delete_profile, name='delete_profile'),

    # path('activateaccount/', views.activate_account, name='activate_account'),
    path('activate/<str:token>/', views.activate_account, name='activate_account'),
    
    path('forgotpassword/', views.forgot_password, name='forgot_password'),
    path('resetpassword/<str:user_id>/<str:token>/<str:user_email>/', views.reset_password, name='reset_password'),
    # path('savefeedback', views.save_feedback, name='save_feedback'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
