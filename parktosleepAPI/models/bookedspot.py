from django.db import models


class BookedSpot(models.Model):

    renter = models.ForeignKey("Rentee", on_delete=models.CASCADE)
    rental_spot = models.ForeignKey("RentalPost", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
