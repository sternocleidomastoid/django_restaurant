from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest

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
        if form.instance.status == 'retracted_inventory':
            ingredients = MenuItem.objects.get(name=form.instance.menu_item).ingredients.all()
            for ingredient in ingredients:
                ingredient.name.add(ingredient.quantity)
        return super().form_valid(form)
