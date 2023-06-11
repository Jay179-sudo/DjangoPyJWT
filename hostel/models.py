from django.db import models


# Create your models here.
class Hostel(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    hostel_code = models.CharField(max_length=5)
    capacity = models.IntegerField()

