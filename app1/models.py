from django.db import models


# Create your models here.

class PizzaModel(models.Model):
    name = models.CharField(max_length=10)
    price = models.CharField(max_length=10)


class customermodel(models.Model):
    userid = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    usermail = models.CharField(max_length=25, default="singhswapnil507@gmail.com")


class OrderModel(models.Model):
    username = models.CharField(max_length=20)
    phoneno = models.CharField(max_length=10)
    address = models.CharField(max_length=10)
    ordereditems = models.CharField(max_length=30)
    status = models.CharField(max_length=10, default="Waiting for confirmation", editable=True)
