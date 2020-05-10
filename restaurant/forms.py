from django.forms import ModelForm, forms

from restaurant.models import Sale, MenuItem, Transaction


class SaleForm(ModelForm):

    class Meta:
        model = Sale
        fields = ['menu_item', 'quantity']

    def clean(self):
        for ingredient in self.cleaned_data["menu_item"].ingredients.all():
            if not ingredient.is_inventory_sufficient(self.cleaned_data["quantity"]):
                raise forms.ValidationError("Ingredient {} is insufficient or empty".format(ingredient.name.name))
        return self.cleaned_data


class UpdateSaleForm(ModelForm):

    class Meta:
        model = Sale
        fields = ['status', 'note']

    def clean(self):
        if self.instance.status == "retracted_inventory" or self.instance.status == "pre_valid":
            raise forms.ValidationError("Cannot change from 'retracted_inventory' or 'pre_valid', "
                                        "You can make another sale instead")
        return self.cleaned_data


class UpdateTransactionForm(ModelForm):

    class Meta:
        model = Transaction
        fields = ['status', 'note']

    def clean(self):
        if self.instance.status == "retracted_inventory" or self.instance.status == "pre_valid":
            raise forms.ValidationError("Cannot change from 'retracted_inventory' or 'pre_valid', "
                                        "You can make another transaction instead")
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



