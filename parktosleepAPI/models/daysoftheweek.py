from django.db import models


class DaysOfTheWeek(models.Model):

    day = models.CharField(max_length=100)
