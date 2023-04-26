from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


cC

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=30, default='')
    password = models.CharField(max_length=20)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Color(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    pastel = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Event(models.Model):
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    userId = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    start = models.IntegerField(validators=[MaxValueValidator(95), MinValueValidator(0)])
    end = models.IntegerField(validators=[MaxValueValidator(96), MinValueValidator(1)])
    date = models.DateField(default=datetime.date.today)
    sentMail = models.BooleanField(default=False)