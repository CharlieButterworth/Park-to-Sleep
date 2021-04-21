from django.db import models


class BookedSpot(models.Model):

    renter = models.ForeignKey("Rentee", on_delete=models.CASCADE)
    rental_spot = models.ForeignKey("RentalPost", on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)

    @property
    def is_current_user(self):
        return self.__is_current_user

    @is_current_user.setter
    def is_current_user(self, value):
        self.__is_current_user = value
