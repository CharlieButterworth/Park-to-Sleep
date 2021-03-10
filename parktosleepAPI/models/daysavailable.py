from django.db import models


class DaysAvailable(models.Model):

    days = models.ForeignKey("DaysOfTheWeek", on_delete=models.CASCADE)
    rental_post = models.ForeignKey("RentalPost", on_delete=models.CASCADE)
