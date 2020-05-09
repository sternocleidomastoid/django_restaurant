from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from restaurant.models import Sale, MenuItem


class SaleListView(ListView):
    model = Sale
    template_name = 'restaurant/sale/sale_list.html'
    ordering = ['-transaction']


class SaleDetailView(DetailView):
    model = Sale
    template_name = 'restaurant/sale/sale_detail.html'


class SaleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Sale
    template_name = 'restaurant/sale/sale_form.html'
    fields = ['status', 'note']

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.change_status(form.instance.status)
        return super().form_valid(form)
