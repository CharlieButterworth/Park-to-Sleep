from django.db import models
from django.contrib.auth.models import User


class Rentee(models.Model):

    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    phone = models.IntegerField()
    pts_user = models.ForeignKey(User, on_delete=models.CASCADE)
