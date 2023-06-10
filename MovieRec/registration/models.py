from django.db import models
from django.contrib.auth.models import User

class Film(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    rate = models.IntegerField()
    
    
class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=255)
    is_watched = models.BooleanField(default=False)
