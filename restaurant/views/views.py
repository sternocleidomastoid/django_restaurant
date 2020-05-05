import decimal

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from restaurant.forms import SaleForm
from restaurant.models import Transaction, MenuItem, Sale


def home(request):
    return render(request, 'restaurant/home.html')


def about(request):
    return render(request, 'restaurant/about.html', {'title': 'amonamon'})


@login_required()
def process_transaction(request):
    if request.method == "POST" and request.POST.get('trans_id__ftotal'):
        form = SaleForm(request.POST)
        ftotal, trans_id = _get_ftotal_and_trans_id_from_post(request)
        rtotal = ftotal
        if form.is_valid():
            _update_db_values(rtotal, trans_id)
        return redirect('restaurant-transactions')
    elif request.method == "POST" and request.POST.get('trans_id__rtotal'):
        form, rtotal, trans_id = _process_sale_addition(request)
    else:
        trans = _add_new_transaction_to_db(request)
        form, rtotal, trans_id = _get_initial_values_for_template(trans)
    return render(request, 'restaurant/process_transaction.html', {'form': form, 'trans_id': trans_id, 'rtotal': rtotal})


def _update_db_values(rtotal, trans_id):
    for sale in Sale.objects.filter(transaction=trans_id):
        _decrement_inventory_and_validate_sale(sale)
    _update_trans_fields(rtotal, trans_id)


def _process_sale_addition(request):
    form = SaleForm(request.POST)
    rtotal, trans_id = _get_rtotal_and_trans_id_from_post(request)
    if form.is_valid():
        rtotal = _increment_running_total(form, rtotal, trans_id)
        form.save()
    return form, rtotal, trans_id


def _decrement_inventory_and_validate_sale(sale):
    for ingredient in sale.menu_item.ingredients.all():
        ingredient.name.deduct(ingredient.quantity * sale.quantity)
    sale.change_status('valid')


def _update_trans_fields(rtotal, trans_id):
    trans = Transaction.objects.get(id=trans_id)
    trans.change_status('valid')
    trans.update_total_price(rtotal)


def _get_initial_values_for_template(trans):
    trans_id = trans.id
    rtotal = 0
    form = SaleForm()
    return form, rtotal, trans_id


def _add_new_transaction_to_db(request):
    trans = Transaction(cashier=request.user, total_price=0)
    trans.save()
    return trans


def _increment_running_total(form, rtotal, trans_id):
    amount = form.cleaned_data.get('quantity')
    price = MenuItem.objects.get(name=form.instance.menu_item).price
    form.instance.transaction_id = trans_id
    rtotal += amount * price
    return rtotal


def _get_rtotal_and_trans_id_from_post(request):
    trans_id, rtotal = request.POST.get('trans_id__rtotal').split("__")
    trans_id = int(trans_id)
    rtotal = decimal.Decimal(rtotal)
    return rtotal, trans_id

def _get_ftotal_and_trans_id_from_post(request):
    trans_id, ftotal = request.POST.get('trans_id__ftotal').split("__")
    trans_id = int(trans_id)
    ftotal = decimal.Decimal(ftotal)
    return ftotal, trans_id




