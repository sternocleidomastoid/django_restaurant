from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from mixer.auto import mixer
import pytest

from restaurant.models import MenuItem, Inventory, Ingredient, Sale, Transaction


@pytest.mark.integration
class TestTransactionFormsUpdate(TestCase):

    def setUp(self):
        self.staff_user = mixer.blend(User, is_staff=True)
        self.staff_user.set_password('test123')
        self.staff_user.save()
        self.client.login(username=self.staff_user.username, password='test123')

    def test__valid_update__db_entry_changes_including_sale(self):
        trans = mixer.blend(Transaction, note='original note', status='valid')
        sale = mixer.blend(Sale, transaction=trans, note="original note", status='valid')
        new_fields = {'status': 'retracted', 'note': 'updated note'}

        self.client.post(reverse_lazy('restaurant-transaction-update', kwargs={'pk': trans.pk}), new_fields)

        trans.refresh_from_db()

        self.assertEqual(trans.status, 'retracted')
        self.assertEqual(trans.note, 'updated note')

        sale.refresh_from_db()

        self.assertEqual(sale.status, 'retracted')
        self.assertEqual(sale.note, 'updated note')

    def test__valid_update_status_to_retracted_inventory__adds_inventory(self):
        inv1 = mixer.blend(Inventory, total=21)
        inv2 = mixer.blend(Inventory, total=10)
        ing1 = mixer.blend(Ingredient, name=inv1, quantity=20.0)
        ing2 = mixer.blend(Ingredient, name=inv2, quantity=15.0)
        menu1 = mixer.blend(MenuItem, name='spaghetti', ingredients=[ing1], price=5.25)
        menu2 = mixer.blend(MenuItem, name='carbonara', ingredients=[ing1, ing2], price=5.25)
        trans = mixer.blend(Transaction, note='original note', status='valid')
        sale1 = mixer.blend(Sale, transaction=trans, menu_item=menu1, quantity=2, status='valid')
        sale2 = mixer.blend(Sale, transaction=trans, menu_item=menu2, quantity=1, status='valid')
        new_fields = {'status': 'retracted_inventory', 'note': 'updated note'}

        self.client.post(reverse_lazy('restaurant-transaction-update', kwargs={'pk': trans.pk}), new_fields)

        trans.refresh_from_db()

        self.assertEqual(trans.status, 'retracted_inventory')
        self.assertEqual(trans.note, 'updated note')

        sale1.refresh_from_db()
        self.assertEqual(sale1.status, 'retracted_inventory')
        self.assertEqual(sale1.note, 'updated note')
        sale2.refresh_from_db()
        self.assertEqual(sale2.status, 'retracted_inventory')
        self.assertEqual(sale2.note, 'updated note')
        self.assertEqual(inv1.get_total(), 81)
        self.assertEqual(inv2.get_total(), 25)

    def test__invalid_update__currently_retracted_inventory_nor_pre_valid_wont_change_through_form_incl_sale(self):
        trans = mixer.blend(Transaction, note="original note", status='retracted_inventory')
        sale = mixer.blend(Sale, transaction=trans, note="original note", status='valid')
        new_fields = {'status': 'retracted', 'note': 'updated note'}
        response = self.client.post(reverse_lazy('restaurant-transaction-update', kwargs={'pk': trans.pk}), new_fields)

        trans.refresh_from_db()
        self.assertEqual(trans.status, 'retracted_inventory')
        self.assertEqual(trans.note, 'original note')
        self.assertIn("Cannot change from 'retracted_inventory' or 'pre_valid', "
                      "You can make another transaction instead", response.context['form'].errors['__all__'])
        sale.refresh_from_db()
        self.assertEqual(sale.status, 'valid')
        self.assertEqual(sale.note, 'original note')

        trans = mixer.blend(Transaction, note="original note", status='pre_valid')
        sale = mixer.blend(Sale, transaction=trans, note="original note", status='valid')
        new_fields = {'status': 'retracted', 'note': 'updated note'}
        response = self.client.post(reverse_lazy('restaurant-transaction-update', kwargs={'pk': trans.pk}), new_fields)

        trans.refresh_from_db()
        self.assertEqual(trans.status, 'pre_valid')
        self.assertEqual(trans.note, 'original note')
        self.assertIn("Cannot change from 'retracted_inventory' or 'pre_valid', "
                      "You can make another transaction instead", response.context['form'].errors['__all__'])
        sale.refresh_from_db()
        self.assertEqual(sale.status, 'valid')
        self.assertEqual(sale.note, 'original note')

    def test__invalid_update__missing_note_db_entry_does_not_change(self):
        trans = mixer.blend(Transaction, note='original note', status='valid')
        new_fields = {'status': 'retracted', 'note': ''}

        response = self.client.post(reverse_lazy('restaurant-transaction-update', kwargs={'pk': trans.pk}), new_fields)

        trans.refresh_from_db()
        self.assertEqual(trans.status, 'valid')
        self.assertEqual(trans.note, 'original note')
        self.assertIn('This field is required.', response.context['form']['note'].errors)
