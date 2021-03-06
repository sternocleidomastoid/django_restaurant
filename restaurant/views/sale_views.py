from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from restaurant.forms import UpdateSaleForm
from restaurant.models import Sale


class SaleListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Sale
    template_name = 'restaurant/sale/sale_list.html'
    ordering = ['-transaction']

    def test_func(self):
        return self.request.user.is_staff


class SaleDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Sale
    template_name = 'restaurant/sale/sale_detail.html'

    def test_func(self):
        return self.request.user.is_staff


class SaleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Sale
    template_name = 'restaurant/sale/sale_form.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_form_class(self):
        return UpdateSaleForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.change_status(form.instance.status)
        return super().form_valid(form)
