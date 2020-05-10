from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from mixer.auto import mixer

from restaurant.models import MenuItem, Inventory, Ingredient, Sale, Transaction


class TestSaleFormsUpdate(TestCase):

    def setUp(self):
        self.staff_user = mixer.blend(User, is_staff=True)
        self.staff_user.set_password('test123')
        self.staff_user.save()
        self.client.login(username=self.staff_user.username, password='test123')

    def test__valid_update__db_entry_changes(self):
        transaction = mixer.blend(Transaction)
        sale = mixer.blend(Sale, transaction=transaction, note="original note", status='valid')
        new_fields = {'status': 'retracted', 'note': 'updated note'}

        self.client.post(reverse_lazy('restaurant-sale-update', kwargs={'pk': sale.pk}), new_fields)
        sale.refresh_from_db()
        self.assertEqual(sale.status, 'retracted')
        self.assertEqual(sale.note, 'updated note')

    def test__valid_update_status_to_retracted_inventory__adds_inventory(self):
        inv1 = mixer.blend(Inventory, total=21)
        ing1 = mixer.blend(Ingredient, name=inv1, quantity=20.0)
        inv2 = mixer.blend(Inventory, total=10)
        ing2 = mixer.blend(Ingredient, name=inv2, quantity=15.0)
        menu = mixer.blend(MenuItem, name='spaghetti', ingredients=[ing1, ing2], price=5.25)
        transaction = mixer.blend(Transaction)
        sale = mixer.blend(Sale, transaction=transaction, menu_item=menu,
                           quantity=2, note="original note", status='valid')
        new_fields = {'status': 'retracted_inventory', 'note': 'updated note'}

        self.client.post(reverse_lazy('restaurant-sale-update', kwargs={'pk': sale.pk}), new_fields)

        sale.refresh_from_db()
        self.assertEqual(sale.status, 'retracted_inventory')
        self.assertEqual(inv1.get_total(), 61)
        self.assertEqual(inv2.get_total(), 40)

    def test__invalid_update__currently_retracted_inventory_nor_pre_valid_wont_change_through_form(self):
        transaction = mixer.blend(Transaction)
        sale = mixer.blend(Sale, transaction=transaction, note="original note", status='retracted_inventory')
        new_fields = {'status': 'retracted', 'note': 'updated note'}
        response = self.client.post(reverse_lazy('restaurant-sale-update', kwargs={'pk': sale.pk}), new_fields)

        sale.refresh_from_db()
        self.assertEqual(sale.status, 'retracted_inventory')
        self.assertEqual(sale.note, 'original note')
        self.assertIn("Cannot change from 'retracted_inventory' or 'pre_valid', "
                      "You can make another sale instead", response.context['form'].errors['__all__'])

        sale = mixer.blend(Sale, transaction=transaction, note="original note", status='pre_valid')
        new_fields = {'status': 'retracted', 'note': 'updated note'}
        response = self.client.post(reverse_lazy('restaurant-sale-update', kwargs={'pk': sale.pk}), new_fields)

        sale.refresh_from_db()
        self.assertEqual(sale.status, 'pre_valid')
        self.assertEqual(sale.note, 'original note')
        self.assertIn("Cannot change from 'retracted_inventory' or 'pre_valid', "
                      "You can make another sale instead", response.context['form'].errors['__all__'])

    def test__invalid_update__missing_note_db_entry_does_not_change(self):
        transaction = mixer.blend(Transaction)
        sale = mixer.blend(Sale, transaction=transaction, note="original note", status='valid')
        new_fields = {'status': 'retracted', 'note': ''}

        response = self.client.post(reverse_lazy('restaurant-sale-update', kwargs={'pk': sale.pk}), new_fields)

        sale.refresh_from_db()
        self.assertEqual(sale.status, 'valid')
        self.assertEqual(sale.note, 'original note')
        self.assertIn('This field is required.', response.context['form']['note'].errors)
