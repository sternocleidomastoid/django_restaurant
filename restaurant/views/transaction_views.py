from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from restaurant.models import Transaction, Sale


class TransactionListView(ListView):
    model = Transaction
    template_name = 'restaurant/transaction/transaction_list.html'
    ordering = ['-status']

    def get(self, request, *args, **kwargs):
        Transaction.delete_prevalid_transactions()
        return super().get(request, *args, **kwargs)


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
        for sale in Sale.objects.filter(transaction=self.kwargs['pk']):
            sale.change_status(form.instance.status)
            sale.change_note(form.instance.note)
        return super().form_valid(form)
