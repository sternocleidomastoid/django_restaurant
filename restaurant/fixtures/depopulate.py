from restaurant.models import Ingredient, Inventory, MenuItemType, MenuItem, Sale, InventoryTopUp, Transaction


def depopulate():
    Inventory.objects.all().delete()
    Ingredient.objects.all().delete()
    MenuItemType.objects.all().delete()
    MenuItem.objects.all().delete()
    Sale.objects.all().delete()
    InventoryTopUp.objects.all().delete()
    Transaction.objects.all().delete()
