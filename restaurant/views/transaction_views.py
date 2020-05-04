from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest

#from restaurant.forms import SaleFormSet
from restaurant.models import Transaction


class TransactionListView(ListView):
    model = Transaction
    template_name = 'restaurant/transaction/transaction_list.html'
    ordering = ['-date']


class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'restaurant/transaction/transaction_detail.html'


# class TransactionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
#     model = Transaction
#     template_name = 'restaurant/transaction/transaction_form.html'
#     fields = []
#     success_url = None
#
#     def get_context_data(self, **kwargs):
#         data = super(TransactionCreateView, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['sales'] = SaleFormSet(self.request.POST)
#         else:
#             data['sales'] = SaleFormSet()
#         return data
#
#     def form_valid(self, form):
#         form.instance.total_price = 100
#         context = self.get_context_data()
#         sales = context['sales']
#         with transaction.atomic():
#             form.instance.cashier = self.request.user
#             self.object = form.save()
#
#             if sales.is_valid():
#                 sales.instance = self.object
#
#                 sales.save()
#         return super(TransactionCreateView, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('restaurant-menuitems')
#
#     def test_func(self):
#         return self.request.user.is_staff
