from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from restaurant.forms import SaleForm
from restaurant.models import Transaction
from restaurant.views.sale_views import SaleCreateView


def home(request):
    return render(request, 'restaurant/home.html')


def about(request):
    return render(request, 'restaurant/about.html', {'title': 'amonamon'})


def process_transaction(request):
    #cashier = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    #note = models.TextField(blank=True)
    #date = models.DateField(default=timezone.now)
    #total_price
    # trans = Transaction()
    # trans.save()
    form = SaleForm



