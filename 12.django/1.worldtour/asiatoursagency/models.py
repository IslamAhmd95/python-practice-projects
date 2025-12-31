from sys import maxsize
from django.db import models

# Create your models here.
class Tour(models.Model):
    origin_country = models.CharField(max_length=64)
    destination_country = models.CharField(max_length=64)
    number_of_nights = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"id: {self.id}, From {self.origin_country} to {self.destination_country} for {self.number_of_nights} costs ${self.price}"