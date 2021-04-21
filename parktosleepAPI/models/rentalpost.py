from django.db import models


class RentalPost(models.Model):

    rentee = models.ForeignKey("Rentee", on_delete=models.CASCADE)
    max_length = models.IntegerField()
    description = models.CharField(max_length=350)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    start_time = models.DateField(auto_now=False, auto_now_add=False)
    end_time = models.DateField(auto_now=False, auto_now_add=False)

    @property
    def is_current_user(self):
        return self.__is_current_user

    @is_current_user.setter
    def is_current_user(self, value):
        self.__is_current_user = value
