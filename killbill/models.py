from django.db import models

# Create your models here.

class UserGroup(models.Model):
    address       = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.address


class Person(models.Model):
    name           = models.CharField(max_length=40)
    group          = models.ForeignKey(UserGroup)
    def __str__(self):
        return self.name


class Shop(models.Model):
    delivery_date  = models.DateField()
    group          = models.ForeignKey(UserGroup)
    def __str__(self):
        return str(self.delivery_date)


class Item(models.Model):
    name           = models.CharField(max_length=100, unique=True)
    price          = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return self.name


class ItemFromShop(models.Model):
    item           = models.ForeignKey(Item)
    shop           = models.ForeignKey(Shop)
    def __str__(self):
        return "%s from shop %s" % (self.item, self.shop)


class ItemFromShopToPerson(models.Model):
    item_from_shop = models.ForeignKey(ItemFromShop)
    person         = models.ForeignKey(Person)
    quantity       = models.PositiveIntegerField()
    def __str__(self):
        return "%s, of which %s bought %d" % (self.item_from_shop, self.person, self.quantity)






