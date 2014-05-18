from django.db import models

# Create your models here.

class UserGroup(models.Model):
    address       = models.CharField(max_length=100)
    def __str__(self):
        return self.address


class Person(models.Model):
    name          = models.CharField(max_length=40)
    group         = models.ForeignKey(UserGroup)
    def __str__(self):
        return self.name


class Shop(models.Model):
    delivery_date = models.DateField()
    group         = models.ForeignKey(UserGroup)
    def __str__(self):
        return str(self.delivery_date)


class Item(models.Model):
    name          = models.CharField(max_length=100)
    price         = models.DecimalField(max_digits=5, decimal_places=2)
    shop          = models.ManyToManyField(Shop)
    person        = models.ManyToManyField(Person)
    def __str__(self):
        return self.name