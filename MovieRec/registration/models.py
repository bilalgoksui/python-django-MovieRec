from django.db import models
from django.contrib.auth.models import User

class Film(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=255, blank=False, null=False)
    comment = models.CharField(max_length=255, blank=False, null=False)
    rate = models.IntegerField(blank=False, null=False)
    
    
class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=255)
    is_watched = models.BooleanField(default=False)


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    smilar_movie = models.CharField(max_length=255, blank=False, null=False)
    mood_text = models.CharField(max_length=255, blank=False, null=False)
    movie_name = models.CharField(max_length=255, blank=False, null=False)
    imdb_title = models.CharField(max_length=255, blank=False, null=False)
    genres = models.CharField(max_length=255, blank=False, null=False)
    genres_match = models.IntegerField(blank=False, null=False)
    feedback = models.BooleanField(default=False)