from django.forms import ModelForm, forms
from django.forms.models import inlineformset_factory
from django.http import HttpResponseBadRequest

from restaurant.models import Sale, Transaction, MenuItem


class SaleForm(ModelForm):

    class Meta:
        model = Sale
        fields = ['menu_item', 'quantity']

    def clean(self):
        for ingredient in self.cleaned_data["menu_item"].ingredients.all():
            if not self._inventory_level_passes(ingredient, self.cleaned_data["quantity"]):
                raise forms.ValidationError("Ingredient {} is insufficient or empty".format(ingredient.name.name))
        return self.cleaned_data

    def _inventory_level_passes(self, ingredient, menu_quantity):
        if ingredient.name.get_total() == 0:
            # disable all menus with the specific inventory
            return False
        if ingredient.name.get_total() < ingredient.quantity * menu_quantity:
            return False
        return True
