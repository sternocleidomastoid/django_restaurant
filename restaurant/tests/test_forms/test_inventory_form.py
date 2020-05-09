from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from mixer.auto import mixer

from restaurant.models import Inventory


class TestInventoryFormsCreate(TestCase):

    def setUp(self):
        self.staff_user = mixer.blend(User, is_staff=True)
        self.staff_user.set_password('test123')
        self.staff_user.save()
        self.client.login(username=self.staff_user.username, password='test123')

    def test__valid_input__means_db_increments_by_one(self):
        self.client.post(reverse_lazy('restaurant-inventory-create'),
                         {'name': "oil", 'total': 10.0, 'low_level_threshold': 10.0, 'price': 1.0, 'unit': 'ml'})

        self.assertEqual(Inventory.objects.count(), 1)

    def test__invalid_missing_required_field__does_not_add_in_db(self):
        response = self.client.post(reverse_lazy('restaurant-inventory-create'),
                                    {'name': "oil", 'total': 10.0, 'low_level_threshold': 10.0, 'price': 1.0})

        self.assertIn('This field is required.', response.context['form']['unit'].errors)
        self.assertEqual(Inventory.objects.count(), 0)


class TestInventoryFormsUpdate(TestCase):

    def setUp(self):
        self.staff_user = mixer.blend(User, is_staff=True)
        self.staff_user.set_password('test123')
        self.staff_user.save()
        self.client.login(username=self.staff_user.username, password='test123')
        self.inv = mixer.blend(Inventory, name="oil", total=10.0, low_level_threshold=10.0, price=1.0, unit='ml')

    def test__valid_input__means_db_entry_changes(self):
        new_fields = {'name': self.inv.name, 'total': 99.0, 'low_level_threshold': 100.0,
                      'price': self.inv.price, 'unit': 'kg'}

        self.client.post(reverse_lazy('restaurant-inventory-update', kwargs={'pk': self.inv.pk}),
                         new_fields)

        self.inv.refresh_from_db()
        self.assertEqual(self.inv.total, 99)
        self.assertEqual(self.inv.low_level_threshold, 100)
        self.assertEqual(self.inv.price, 1)
        self.assertEqual(self.inv.unit, 'kg')

    def test__invalid_blank_required_field__does_not_change_db_entry(self):
        response = self.client.post(reverse_lazy('restaurant-inventory-update', kwargs={'pk': self.inv.pk}),
                                    {'total': 99.0, 'low_level_threshold': 100.0, 'unit': ''})

        self.inv.refresh_from_db()
        self.assertEqual(self.inv.total, 10)
        self.assertEqual(self.inv.low_level_threshold, 10)
        self.assertEqual(self.inv.price, 1)
        self.assertEqual(self.inv.unit, 'ml')
        self.assertIn('This field is required.', response.context['form']['unit'].errors)


