from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from restaurant.models import Inventory


class InventoryListView(ListView):
    model = Inventory
    template_name = 'restaurant/inventory/inventory_list.html'
    ordering = ['name']


class InventoryDetailView(DetailView):
    model = Inventory
    template_name = 'restaurant/inventory/inventory_detail.html'


class InventoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Inventory
    template_name = 'restaurant/inventory/inventory_form.html'
    fields = ['name', 'total', 'low_level_threshold', 'price', 'unit']

    def test_func(self):
        return self.request.user.is_staff


class InventoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Inventory
    template_name = 'restaurant/inventory/inventory_form.html'
    fields = ['name', 'total', 'low_level_threshold', 'price', 'unit']

    def test_func(self):
        return self.request.user.is_staff


class InventoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Inventory
    template_name = 'restaurant/inventory/inventory_confirm_delete.html'
    success_url = reverse_lazy('restaurant-inventories')

    def test_func(self):
        return self.request.user.is_staff
