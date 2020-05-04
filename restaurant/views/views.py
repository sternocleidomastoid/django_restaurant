import decimal

from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from restaurant.forms import SaleForm
from restaurant.models import Transaction, MenuItem


def home(request):
    return render(request, 'restaurant/home.html')


def about(request):
    return render(request, 'restaurant/about.html', {'title': 'amonamon'})


def process_transaction(request):
    if request.method == "POST" and request.POST.get('trans_ftotal'):
        pass
    elif request.method == "POST" and request.POST.get('trans_rtotal'):
        form = SaleForm(request.POST)
        trans, rtotal = request.POST.get('trans_rtotal').split("_")
        trans = int(trans)
        rtotal = decimal.Decimal(rtotal)
        if form.is_valid():
            amount = form.cleaned_data.get('quantity')
            price = MenuItem.objects.get(name=form.instance.menu_item).price
            form.instance.transaction_id = trans
            rtotal += amount*price
            form.save()
    else:
        trans = Transaction(cashier=request.user, total_price=0)
        trans.save()
        trans = trans.id
        rtotal = 0
        form = SaleForm()
    return render(request, 'restaurant/sale/sale_form.html', {'form': form, 'trans': trans, 'rtotal': rtotal})




