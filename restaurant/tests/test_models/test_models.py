from unittest.mock import patch, call

from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse

from restaurant.models import Ingredient, Inventory, MenuItemType, MenuItem, Sale, InventoryTopUp, Transaction
from mixer.backend.django import mixer


class InventoryTestCase(TestCase):

    def test_instance(self):
        i = mixer.blend(Inventory)
        self.assertEqual(i.__str__(), i.name)
        self.assertTrue(isinstance(i, Inventory))

    def test_absolute_url(self):
        i = mixer.blend(Inventory)
        self.assertEqual(i.get_absolute_url(), reverse('restaurant-inventory-detail', args=[str(i.pk)]))

    def test__is_low_level__should_return_true_if_quantity_lower_than_threshold(self):
        i = mixer.blend(Inventory, low_level_threshold=10.0, total=5.0)
        self.assertTrue(i.is_low_level())
        i = mixer.blend(Inventory, low_level_threshold=10.0, total=15.0)
        self.assertFalse(i.is_low_level())

    def test__add__should_add_to_total(self):
        i = mixer.blend(Inventory, low_level_threshold=10.0, total=5.0)
        self.assertEqual(i.get_total(), 5.0)
        i.add(25.0)
        self.assertEqual(i.get_total(), 30.0)

    def test__deduct__should_deduct_to_total(self):
        i = mixer.blend(Inventory, low_level_threshold=10.0, total=25.0)
        self.assertEqual(i.get_total(), 25.0)
        i.deduct(20.0)
        self.assertEqual(i.get_total(), 5.0)


class IngredientTestCase(TestCase):

    def test_instance(self):
        inv = mixer.blend(Inventory)
        ing = mixer.blend(Ingredient, name=inv, quantity=10.0)

        self.assertTrue(isinstance(ing, Ingredient))
        self.assertEqual(ing.__str__(), '{} {} {}'.format(inv.name, 10.0, inv.unit))

    def test_absolute_url(self):
        i = mixer.blend(Ingredient)
        self.assertEqual(i.get_absolute_url(), reverse('restaurant-ingredient-detail', args=[str(i.pk)]))


class MenuItemTestCase(TestCase):

    def test_instance(self):
        u = mixer.blend(User)
        m = mixer.blend(MenuItem, author=u)
        self.assertEqual(m.status, "disabled")
        self.assertEqual(m.__str__(), m.name)

        ing_set = [mixer.blend(Ingredient) for _ in range(2)]
        for ing in ing_set:
            m.ingredients.add(ing)
        self.assertEqual(ing_set, [i for i in m.ingredients.all()])

    def test_absolute_url(self):
        m = mixer.blend(MenuItem)
        self.assertEqual(m.get_absolute_url(), reverse('restaurant-menuitem-detail', args=[str(m.pk)]))


class MenuItemTypeTestCase(TestCase):

    def test_instance(self):
        m = mixer.blend(MenuItemType)
        self.assertTrue(isinstance(m, MenuItemType))
        self.assertEqual(m.__str__(), m.name)

        menu_set = [mixer.blend(MenuItem) for _ in range(2)]
        for menu in menu_set:
            m.menu_items.add(menu)
        self.assertEqual(menu_set, [i for i in m.menu_items.all()])


class SaleTestCase(TestCase):

    def test_instance(self):
        s = mixer.blend(Sale)
        self.assertTrue(isinstance(s, Sale))
        self.assertEqual(s.status, 'pre_valid')

    def test__change_status(self):
        s = mixer.blend(Sale, status='pre_valid')
        self.assertEqual(s.status, 'pre_valid')
        s.change_status('valid')
        self.assertEqual(s.status, 'valid')

    def test_absolute_url(self):
        s = mixer.blend(Sale)
        self.assertEqual(s.get_absolute_url(), reverse('restaurant-sale-detail', args=[str(s.pk)]))


class TransactionTestCase(TestCase):

    def test_instance(self):
        t = mixer.blend(Transaction)
        self.assertTrue(isinstance(t, Transaction))
        self.assertEqual(t.status, 'pre_valid')
        self.assertEqual(t.__str__(), str(t.id))

    def test__change_status(self):
        t = mixer.blend(Transaction, status='pre_valid')
        self.assertEqual(t.status, 'pre_valid')
        t.change_status('valid')
        self.assertEqual(t.status, 'valid')

    def test_absolute_url(self):
        t = mixer.blend(Transaction)
        self.assertEqual(t.get_absolute_url(), reverse('restaurant-transaction-detail', args=[str(t.pk)]))

    def test__update_total_price__works(self):
        t = mixer.blend(Transaction, total_price=10)
        self.assertEqual(t.total_price, 10.0)
        t.update_total_price(15)
        self.assertEqual(t.total_price, 15.0)

    @patch('restaurant.models.Transaction.objects')
    def test__delete_prevalid_transactions__works(self, mock_objects):
        Transaction.delete_prevalid_transactions()
        mock_objects.assert_has_calls([call.filter(status='pre_valid'), call.filter().delete()])


class InventoryTopUpTestCase(TestCase):

    def test_instance(self):
        d = mixer.blend(InventoryTopUp)
        self.assertTrue(isinstance(d, InventoryTopUp))

    def test__delete_encoder__raises_ProtectedError(self):
        u = mixer.blend(User)
        mixer.blend(InventoryTopUp, encoder=u)
        with self.assertRaises(ProtectedError):
            u.delete()
