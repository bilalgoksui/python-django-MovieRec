from django.contrib import admin
from .models import Feedback, Film , WatchList

admin.site.register(Film)
admin.site.register(WatchList)
admin.site.register(Feedback)