from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200, default='')
    kontenti = models.CharField(max_length=200, default='')
    ball = models.CharField(max_length=200, default='bal')
