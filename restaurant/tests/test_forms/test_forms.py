from django.test import TestCase
from mixer.auto import mixer

from restaurant.forms import SaleForm, UpdateMenuItemForm
from restaurant.models import MenuItem, Inventory, Ingredient
import pytest


@pytest.mark.unit
class SaleFormTests(TestCase):
    def test__correct_data__validates(self):
        m = mixer.blend(MenuItem, status='available')
        form_data = {'menu_item': m.id, 'quantity': 1}
        form = SaleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test__blank_menu_item__invalidates(self):
        form_data = {'menu_item': '', 'quantity': 1}
        form = SaleForm(data=form_data)
        with self.assertRaises(KeyError):
            form.is_valid()
        self.assertEqual(form.errors['menu_item'], ["This field is required."])

    def test__zero_quantity__invalidates(self):
        m = mixer.blend(MenuItem, status='available')
        form_data = {'menu_item': m.id, 'quantity': 0}
        form = SaleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['quantity'], ['Ensure this value is greater than or equal to 1.'])

    def test__very_large_quantity__invalidates(self):
        m = mixer.blend(MenuItem, status='available')
        form_data = {'menu_item': m.id, 'quantity': 99999}
        form = SaleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['quantity'], ['Ensure this value is less than or equal to 10000.'])

    def test__insufficient_inventory__invalidates(self):
        inv = mixer.blend(Inventory, total=10)
        ing = mixer.blend(Ingredient, name=inv, quantity=5.5)
        m = mixer.blend(MenuItem, status='available', ingredients=[ing])
        form_data = {'menu_item': m.id, 'quantity': 2}
        form = SaleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], ['Ingredient {} is insufficient or empty'.format(ing.name.name)])


@pytest.mark.unit
class UpdateMenuItemFormTestCase(TestCase):

    def test__correct_data__validates(self):
        i = mixer.blend(Ingredient)
        new_data = {'name': 'new_name', 'price': 1.25, 'ingredients': [i.id], 'status': 'disabled'}
        form = UpdateMenuItemForm(data=new_data)
        self.assertTrue(form.is_valid())

    def test__one_missing_data__invalidates(self):
        i = mixer.blend(Ingredient)
        new_data = {'name': 'new_name', 'price': '', 'ingredients': [i.id], 'status': 'disabled'}
        form = UpdateMenuItemForm(data=new_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['price'], ['This field is required.'])

    def test__negative_price__invalidates(self):
        i = mixer.blend(Ingredient)
        new_data = {'name': 'new_name', 'price': -1, 'ingredients': [i.id], 'status': 'disabled'}
        form = UpdateMenuItemForm(data=new_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['price'], ['Ensure this value is greater than or equal to 0.001.'])
