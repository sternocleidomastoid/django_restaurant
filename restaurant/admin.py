from django.contrib import admin
from restaurant.models import Inventory, MenuItem, Sale, Ingredient, MenuItemType, Transaction

# Register your models here.
admin.site.register(Inventory)
admin.site.register(MenuItem)
admin.site.register(Sale)
admin.site.register(Ingredient)
admin.site.register(MenuItemType)
admin.site.register(Transaction)
