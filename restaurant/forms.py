from django.forms import ModelForm, forms

from restaurant.models import Sale, MenuItem


class SaleForm(ModelForm):

    class Meta:
        model = Sale
        fields = ['menu_item', 'quantity']

    def clean(self):
        for ingredient in self.cleaned_data["menu_item"].ingredients.all():
            if not ingredient.is_inventory_sufficient(self.cleaned_data["quantity"]):
                raise forms.ValidationError("Ingredient {} is insufficient or empty".format(ingredient.name.name))
        return self.cleaned_data


class UpdateMenuItemForm(ModelForm):

    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'ingredients', 'status']

    def clean(self):
        if self.cleaned_data['status'] == "available":
            for ingredient in self.cleaned_data["ingredients"]:
                if ingredient.quantity > ingredient.name.get_total():
                    raise forms.ValidationError("Ingredient {} is insufficient".format(ingredient.name.name))
        return self.cleaned_data



