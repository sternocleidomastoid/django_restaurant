from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from mixer.auto import mixer

from restaurant.models import MenuItem, Inventory, Ingredient, Sale, Transaction
import pytest


@pytest.mark.integration
class TestTransactionForms(TestCase):

    def setUp(self):
        self.staff_user = mixer.blend(User, is_staff=True)
        self.staff_user.set_password('test123')
        self.staff_user.save()
        self.client.login(username=self.staff_user.username, password='test123')
        self.inv1 = mixer.blend(Inventory, total=100000)
        self.inv2 = mixer.blend(Inventory, total=100000)
        self.ing1 = mixer.blend(Ingredient, name=self.inv1, quantity=20.0)
        self.ing2 = mixer.blend(Ingredient, name=self.inv2, quantity=15.0)
        self.menu1 = mixer.blend(MenuItem,
                                 name='spaghetti', ingredients=[self.ing1], price=2, status='available')
        self.menu2 = mixer.blend(MenuItem,
                                 name='carbonara', ingredients=[self.ing1, self.ing2], price=3, status='available')

    def test__valid_full_transaction__adds_sales_and_deducts_inventory(self):
        self.client.get(reverse_lazy('restaurant-transaction-create'))
        trans = Transaction.objects.all().first()

        fields = {'menu_item': self.menu1.id, 'quantity': 2, 'add_sale_button_pressed': '{}__0'.format(trans.id)}
        self.client.post(reverse_lazy('restaurant-transaction-create'), fields)

        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Sale.objects.count(), 1)

        fields = {'menu_item': self.menu2.id, 'quantity': 1, 'add_sale_button_pressed': '{}__4'.format(trans.id)}
        self.client.post(reverse_lazy('restaurant-transaction-create'), fields)

        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Sale.objects.count(), 2)

        fields = {'menu_item': self.menu1.id, 'quantity': 2, 'finish_transaction_button_pressed': '{}__7'.format(trans.id)}
        self.client.post(reverse_lazy('restaurant-transaction-create'), fields)

        trans.refresh_from_db()
        self.assertEqual(trans.status, 'valid')
        self.assertEqual(trans.total_price, 7)
        for sale in Sale.objects.all():
            self.assertEqual(sale.transaction, trans)
            self.assertEqual(sale.status, 'valid')
        self.assertEqual(self.inv1.get_total(), 99940)
        self.assertEqual(self.inv2.get_total(), 99985)

    def test__valid_full_transaction__adds_unites_same_sales_and_deducts_inventory(self):
        self.client.get(reverse_lazy('restaurant-transaction-create'))
        trans = Transaction.objects.all().first()

        fields = {'menu_item': self.menu1.id, 'quantity': 1, 'add_sale_button_pressed': '{}__0'.format(trans.id)}
        self.client.post(reverse_lazy('restaurant-transaction-create'), fields)

        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Sale.objects.count(), 1)

        fields = {'menu_item': self.menu1.id, 'quantity': 1, 'add_sale_button_pressed': '{}__4'.format(trans.id)}
        self.client.post(reverse_lazy('restaurant-transaction-create'), fields)

        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Sale.objects.count(), 1)

        fields = {'menu_item': self.menu1.id, 'quantity': 2, 'finish_transaction_button_pressed': '{}__7'.format(trans.id)}
        self.client.post(reverse_lazy('restaurant-transaction-create'), fields)

        trans.refresh_from_db()
        self.assertEqual(trans.status, 'valid')
        self.assertEqual(trans.total_price, 7)
        for sale in Sale.objects.all():
            self.assertEqual(sale.transaction, trans)
            self.assertEqual(sale.status, 'valid')
        self.assertEqual(self.inv1.get_total(), 99960)

    def test__invalid_full_transaction__fails_due_to_unrealistic_total(self):
        self.client.get(reverse_lazy('restaurant-transaction-create'))
        trans = Transaction.objects.all().first()

        fields = {'menu_item': self.menu1.id, 'quantity': 2, 'add_sale_button_pressed': '{}__0'.format(trans.id)}
        self.client.post(reverse_lazy('restaurant-transaction-create'), fields)

        fields = {'menu_item': self.menu1.id, 'quantity': 2,
                  'finish_transaction_button_pressed': '{}__999999'.format(trans.id)}
        response = self.client.post(reverse_lazy('restaurant-transaction-create'), fields)
        self.assertEqual(response.status_code, 400)
