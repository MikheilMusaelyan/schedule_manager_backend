from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


class Post(models.Model):
    title = models.CharField(max_length=200, default='')
    kontenti = models.CharField(max_length=200, default='')
    ball = models.CharField(max_length=200, default='bal')

class Color(models.Model):
    name = models.CharField(max_length=20)
    pastel = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Event(models.Model):
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)

    start = models.IntegerField(validators=[MaxValueValidator(96), MinValueValidator(0)])
    end = models.IntegerField(validators=[MaxValueValidator(96), MinValueValidator(0)])
    date = models.DateField(default=datetime.date.today)