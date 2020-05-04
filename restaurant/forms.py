from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.http import HttpResponseBadRequest

from restaurant.models import Sale, Transaction, MenuItem


class SaleForm(ModelForm):

    class Meta:
        model = Sale
        fields = ['menu_item', 'quantity']

    def form_valid(self, form):
        print('bwahahahahahaha')
        self._set_defaults_for_some_fields(form)
        ingredients = MenuItem.objects.get(name=form.instance.menu_item).ingredients.all()
        for ingredient in ingredients:
            if not self._inventory_level_passes(ingredient, form.instance.quantity):
                return HttpResponseBadRequest("Error: ingredient {} is insufficient or empty".format(
                    ingredient.name.name))
            ingredient.name.deduct(ingredient.quantity * form.instance.quantity)
        return super().form_valid(form)

    def _set_defaults_for_some_fields(self, form):
        form.instance.cashier = self.request.user
        form.instance.transaction_id = Transaction.objects.latest('id').id

    def _inventory_level_passes(self, ingredient, sale_quantity):
        if ingredient.name.get_total == 0:
            # disable all menus with the specific inventory
            return False
        if ingredient.name.get_total() < ingredient.quantity * sale_quantity:
            return False
        return True