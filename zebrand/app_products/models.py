from django.db import models
from django.db.models.fields import IntegerField

# Create your models here.
class Product(models.Model):
    sku = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    price = models.IntegerField()
    brand = models.CharField(max_length=300)

class Admins(models.Model):
    name = models.CharField(max_length=100)
    permissons = models.BooleanField(default=False)
    num_employee = models.IntegerField() 
    password = models.CharField(max_length=50)

