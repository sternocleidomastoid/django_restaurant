from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest

from restaurant.models import Sale, MenuItem


class SaleListView(ListView):
    model = Sale
    template_name = 'restaurant/sale/sale_list.html'


class SaleDetailView(DetailView):
    model = Sale
    template_name = 'restaurant/sale/sale_detail.html'


class SaleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Sale
    template_name = 'restaurant/sale/sale_form.html'
    fields = ['menu_item', 'quantity']

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        self._set_defaults_for_some_fields(form)
        ingredients = MenuItem.objects.get(name=form.instance.menu_item).ingredients.all()
        for ingredient in ingredients:
            if not self._inventory_level_passes(ingredient, form.instance.quantity):
                return HttpResponseBadRequest("Error: ingredient {} is insufficient or empty".format(
                    ingredient.name.name))
            ingredient.name.deduct(ingredient.quantity * form.instance.quantity)
        return super().form_valid(form)

    def post(self, request, format=None):
        pass
        #return Response(request)

    def _set_defaults_for_some_fields(self, form):
        form.instance.cashier = self.request.user
        form.instance.total_price = form.instance.menu_item.price * form.instance.quantity
        form.instance.total_price = round(form.instance.total_price, 2)

    def _inventory_level_passes(self, ingredient, sale_quantity):
        if ingredient.name.get_total == 0:
            # disable all menus with the specific inventory
            return False
        if ingredient.name.get_total() < ingredient.quantity * sale_quantity:
            return False
        return True


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
