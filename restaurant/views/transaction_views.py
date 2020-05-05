from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from restaurant.models import Transaction, Sale


class TransactionListView(ListView):
    model = Transaction
    template_name = 'restaurant/transaction/transaction_list.html'
    ordering = ['-id']


class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'restaurant/transaction/transaction_detail.html'


class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    template_name = 'restaurant/transaction/transaction_form.html'
    fields = ['status', 'note']

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        if form.instance.status == 'retracted_inventory':
            for sale in Sale.objects.filter(transaction=self.kwargs['pk']):
                self._increment_inventory_and_retract_sale(sale)
        return super().form_valid(form)

    def _increment_inventory_and_retract_sale(self, sale):
        for ingredient in sale.menu_item.ingredients.all():
            ingredient.name.add(ingredient.quantity * sale.quantity)
        sale.change_status('valid')
