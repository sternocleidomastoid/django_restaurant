from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest

from restaurant.models import MenuItem


class MenuItemListView(ListView):
    model = MenuItem
    template_name = 'restaurant/menu_item/menuitem_list.html'
    ordering = ['status']


class MenuItemDetailView(DetailView):
    model = MenuItem
    template_name = 'restaurant/menu_item/menuitem_detail.html'


class MenuItemCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MenuItem
    template_name = 'restaurant/menu_item/menuitem_form.html'
    fields = ['name', 'price', 'ingredients']

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class MenuItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MenuItem
    template_name = 'restaurant/menu_item/menuitem_form.html'
    fields = ['name', 'price', 'ingredients', 'status']

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.status == "available":
            for ingredient in form.instance.ingredients.all():
                if ingredient.quantity > ingredient.name.get_total():
                    return HttpResponseBadRequest("Error: ingredient {} is insufficient".format(ingredient.name.name))
        return super().form_valid(form)


class MenuItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MenuItem
    template_name = 'restaurant/menu_item/menuitem_confirm_delete.html'
    success_url = reverse_lazy('restaurant-menuitems')

    def test_func(self):
        return self.request.user.is_staff
