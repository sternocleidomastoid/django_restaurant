from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from restaurant.models import Ingredient


class IngredientListView(ListView):
    model = Ingredient
    template_name = 'restaurant/ingredient/ingredient_list.html'
    ordering = ['name']


class IngredientDetailView(DetailView):
    model = Ingredient
    template_name = 'restaurant/ingredient/ingredient_detail.html'


class IngredientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Ingredient
    template_name = 'restaurant/ingredient/ingredient_form.html'
    fields = ['name', 'quantity']

    def test_func(self):
        return self.request.user.is_staff


class IngredientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ingredient
    template_name = 'restaurant/ingredient/ingredient_form.html'
    fields = ['name', 'quantity']

    def test_func(self):
        return self.request.user.is_staff


class IngredientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ingredient
    template_name = 'restaurant/ingredient/ingredient_confirm_delete.html'
    success_url = reverse_lazy('restaurant-ingredients')

    def test_func(self):
        return self.request.user.is_staff
