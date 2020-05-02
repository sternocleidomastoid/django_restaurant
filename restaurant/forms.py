from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.http import HttpResponseBadRequest

from restaurant.models import Sale, Transaction, MenuItem


class SaleForm(ModelForm):

    class Meta:
        model = Sale
        fields = ['menu_item', 'quantity']


SaleFormSet = inlineformset_factory(
    Transaction, Sale, form=SaleForm,
    fields=['menu_item', 'quantity'], extra=1, can_delete=True
    )
