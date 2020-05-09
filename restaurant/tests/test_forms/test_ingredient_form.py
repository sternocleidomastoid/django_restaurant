from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from mixer.auto import mixer

from restaurant.models import Ingredient, Inventory


class TestIngredientFormsCreate(TestCase):

    def setUp(self):
        self.staff_user = mixer.blend(User, is_staff=True)
        self.staff_user.set_password('test123')
        self.staff_user.save()
        self.client.login(username=self.staff_user.username, password='test123')
        self.inventory_set = [mixer.blend(Inventory) for _ in range(2)]

    def test__valid_input__means_db_increments_by_one(self):
        self.client.post(reverse_lazy('restaurant-ingredient-create'),
                         {'name': self.inventory_set[0].pk, 'quantity': '10.0'})
        self.assertEqual(Ingredient.objects.count(), 1)

    def test__invalid_missing_required_field__does_not_add_in_db(self):
        response = self.client.post(reverse_lazy('restaurant-ingredient-create'),
                                    {'name': self.inventory_set[0].pk})
        self.assertIn('This field is required.', response.context['form']['quantity'].errors)
        self.assertEqual(Ingredient.objects.count(), 0)


class TestIngredientFormsUpdate(TestCase):

    def setUp(self):
        self.staff_user = mixer.blend(User, is_staff=True)
        self.staff_user.set_password('test123')
        self.staff_user.save()
        self.client.login(username=self.staff_user.username, password='test123')
        self.inv_set = [mixer.blend(Inventory) for _ in range(2)]
        self.ing = mixer.blend(Ingredient, name=self.inv_set[0], quantity=10.0)

    def test__valid_input__means_db_entry_changes(self):
        self.new_fields = {'name': self.inv_set[1].pk, 'quantity': 20}

        self.client.post(reverse_lazy('restaurant-ingredient-update', kwargs={'pk': self.ing.pk}), self.new_fields)

        self.ing.refresh_from_db()
        self.assertEqual(self.ing.name, self.inv_set[1])
        self.assertEqual(self.ing.quantity, 20)

    def test__invalid_blank_required_field__does_not_change_db_entry(self):
        self.new_fields = {'name': self.inv_set[1].pk, 'quantity': ''}

        response = self.client.post(reverse_lazy('restaurant-ingredient-update', kwargs={'pk': self.ing.pk}),
                                    self.new_fields)

        self.ing.refresh_from_db()
        self.assertEqual(self.ing.name, self.inv_set[0])
        self.assertEqual(self.ing.quantity, 10)
        self.assertIn('This field is required.', response.context['form']['quantity'].errors)
