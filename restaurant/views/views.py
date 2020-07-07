import decimal

from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from restaurant.forms import SaleForm
from restaurant.models import Transaction, MenuItem, Sale


def home(request):
    Transaction.delete_prevalid_transactions()
    return render(request, 'restaurant/home.html')


def about(request):
    return render(request, 'restaurant/about.html', {'title': 'amonamon'})


@login_required()
def process_transaction(request):
    if request.method == "POST" and request.POST.get('finish_transaction_button_pressed'):
        return _finalize_transaction(request)
    elif request.method == "POST":
        form, running_total, trans_id = _get_request_values_for_add_sale(request)
        running_total = add_sale_to_running_total_if_valid(form, running_total, trans_id)
    else:
        Transaction.delete_prevalid_transactions()
        transaction = _get_new_transaction(request)
        form, running_total, trans_id = _get_initial_values_for_template(transaction)
    curr_sales = Sale.objects.filter(transaction=trans_id)
    return render(request, 'restaurant/process_transaction.html',
                  {'form': form, 'trans_id': trans_id, 'rtotal': running_total, 'curr_sales': curr_sales})


def add_sale_to_running_total_if_valid(form, rtotal, trans_id):
    if form.is_valid():
        form.instance.transaction_id = trans_id
        form.save()
        rtotal = _increment_running_total(form, rtotal)
    return rtotal


def _finalize_transaction(request):
    form, rtotal, ftotal, trans_id = _get_values_for_finishing_transaction(request)
    if not _form_validates_and_transaction_and_inventories_updates_successfully(ftotal, form, trans_id):
        return HttpResponseBadRequest("something went wrong, please double check inputs; total might be too high")
    return redirect('restaurant-transactions')


def _form_validates_and_transaction_and_inventories_updates_successfully(ftotal, form, trans_id):
    transaction = Transaction.objects.get(id=trans_id)
    if form.is_valid() and transaction.total_price_updates_successfully(ftotal):
        _decrement_inventories(trans_id)
        transaction.change_status('valid')
        return True
    return False


def _decrement_inventories(trans_id):
    for sale in Sale.objects.filter(transaction=trans_id):
        for ingredient in sale.menu_item.ingredients.all():
            ingredient.name.deduct(ingredient.quantity * sale.quantity)


def _get_initial_values_for_template(trans):
    trans_id = trans.id
    rtotal = 0
    form = SaleForm()
    return form, rtotal, trans_id


def _get_new_transaction(request):
    trans = Transaction(cashier=request.user, total_price=0)
    trans.save()
    return trans


def _increment_running_total(form, rtotal):
    amount = form.cleaned_data.get('quantity')
    price = MenuItem.objects.get(name=form.instance.menu_item).price
    rtotal += amount * price
    return rtotal


def _get_values_for_finishing_transaction(request):
    form = SaleForm(request.POST)
    trans_id, rtotal = request.POST.get('finish_transaction_button_pressed').split("__")
    trans_id = int(trans_id)
    rtotal = decimal.Decimal(rtotal)
    return form, rtotal, rtotal, trans_id


def _get_request_values_for_add_sale(request):
    form = SaleForm(request.POST)
    trans_id, ftotal = request.POST.get('add_sale_button_pressed').split("__")
    trans_id = int(trans_id)
    ftotal = decimal.Decimal(ftotal)
    return form, ftotal, trans_id
