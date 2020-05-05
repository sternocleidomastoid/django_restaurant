from django.db import models
from django.http import HttpResponseBadRequest
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Inventory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    total = models.FloatField()
    low_level_threshold = models.FloatField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    unit = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('restaurant-inventory-detail', kwargs={'pk': self.pk})

    def is_low_level(self):
        self.refresh_from_db()
        return self.low_level_threshold > self.total

    def get_total(self):
        self.refresh_from_db()
        return self.total

    def deduct(self, amount):
        self.refresh_from_db()
        self.total -= amount
        self.save()

    def add(self, amount):
        self.refresh_from_db()
        self.total += amount
        self.save()


class Ingredient(models.Model):
    name = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        return '{} {} {}'.format(self.name.name, self.quantity, self.name.unit)

    def get_absolute_url(self):
        return reverse('restaurant-ingredient-detail', kwargs={'pk': self.pk})


class MenuItem(models.Model):
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    ingredients = models.ManyToManyField(Ingredient)

    AVAILABLE = 'available'
    UNAVAILABLE = 'unavailable'
    DISABLED = 'disabled'
    STATUS = [
        (AVAILABLE, 'available -- ready to sell menu item'),
        (UNAVAILABLE, 'unavailable -- probably an ingredient is insufficient'),
        (DISABLED, 'disable -- not ready to sell menu item'),
    ]

    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default=DISABLED,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('restaurant-menuitem-detail', kwargs={'pk': self.pk})


class MenuItemType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    menu_items = models.ManyToManyField(MenuItem)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    cashier = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    note = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)

    PRE_VALID = 'pre_valid'
    VALID = 'valid'
    RETRACTED = 'retracted'
    RETRACTED_INVENTORY = 'retracted_inventory'
    STATUS = [
        (PRE_VALID, 'pre_valid'),
        (VALID, 'valid'),
        (RETRACTED, 'retracted -- not counted as valid; cancelled'),
        (RETRACTED_INVENTORY, 'retracted_inventory -- cancelled; undo inventory subtraction')
    ]

    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default=PRE_VALID,
    )

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('restaurant-transaction-detail', kwargs={'pk': self.pk})

    def change_status(self, new_status):
        self.status = new_status
        self.save()

    def update_total_price(self, total_price):
        self.total_price = total_price
        self.save()


class Sale(models.Model):
    transaction = models.ForeignKey(Transaction, related_name="has_sales", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, limit_choices_to={'status': 'available'}, on_delete=models.PROTECT)
    note = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)

    PRE_VALID = 'pre_valid'
    VALID = 'valid'
    RETRACTED = 'retracted'
    RETRACTED_INVENTORY = 'retracted_inventory'
    STATUS = [
        (PRE_VALID, 'pre_valid'),
        (VALID, 'valid'),
        (RETRACTED, 'retracted -- not counted as valid; cancelled'),
        (RETRACTED_INVENTORY, 'retracted_inventory -- cancelled; undo inventory subtraction')
    ]

    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default=PRE_VALID,
    )

    def get_absolute_url(self):
        return reverse('restaurant-sale-detail', kwargs={'pk': self.pk})

    def change_status(self, new_status):
        self.status = new_status
        self.save()


class InventoryTopUp(models.Model):
    name = models.ForeignKey(Inventory, on_delete=models.PROTECT)
    encoder = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    date = models.DateField(default=timezone.now)
    quantity = models.FloatField()
    note = models.CharField(max_length=200)

    VALID = 'valid'
    RETRACTED_INVENTORY = 'retracted_inventory'
    STATUS = [
        (VALID, 'valid'),
        (RETRACTED_INVENTORY, 'retracted_inventory -- cancelled; undo inventory subtraction')
    ]

    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default=VALID,
    )
