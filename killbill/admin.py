from django.contrib import admin
from killbill.models import UserGroup, Person, Shop, Item, ItemFromShop, ItemFromShopToPerson


class PersonInline(admin.TabularInline):
	model = Person
	extra = 2

class ShopInline(admin.TabularInline):
	model = Shop
	extra = 2

class UserGroupAdmin(admin.ModelAdmin):
	inlines = [PersonInline, ShopInline]
	# list_display = ()



admin.site.register(UserGroup, UserGroupAdmin)

admin.site.register(Item)
admin.site.register(ItemFromShop)
admin.site.register(ItemFromShopToPerson)
