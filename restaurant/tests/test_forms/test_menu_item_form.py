from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from mixer.auto import mixer

from restaurant.models import MenuItem, Inventory, Ingredient
import pytest


@pytest.mark.integration
class TestMenuItemFormsCreate(TestCase):

    def setUp(self):
        self.staff_user = mixer.blend(User, is_staff=True)
        self.staff_user.set_password('test123')
        self.staff_user.save()
        self.client.login(username=self.staff_user.username, password='test123')
        self.ing = mixer.blend(Ingredient)

    def test__valid_input__means_db_increments_by_one_and_fills_author_correctly(self):
        self.client.post(reverse_lazy('restaurant-menuitem-create'),
                         {'name': 'spaghetti', 'price': 1.0, 'ingredients': self.ing.pk})

        self.assertEqual(MenuItem.objects.count(), 1)
        self.assertEqual(self.staff_user, MenuItem.objects.get(name='spaghetti').author)

    def test__invalid_missing_required_field__does_not_add_in_db(self):
        response = self.client.post(reverse_lazy('restaurant-menuitem-create'),
                                    {'name': 'spaghetti', 'ingredients': self.ing.pk})
        self.assertIn('This field is required.', response.context['form']['price'].errors)

        self.assertEqual(MenuItem.objects.count(), 0)


@pytest.mark.integration
class TestMenuItemFormsUpdate(TestCase):

    def setUp(self):
        self.staff_user = mixer.blend(User, is_staff=True)
        self.staff_user.set_password('test123')
        self.staff_user.save()
        self.client.login(username=self.staff_user.username, password='test123')

    def test__valid_update__db_entry_changes_including_status_if_sufficient_inventory(self):
        inv1 = mixer.blend(Inventory, total=21)
        inv2 = mixer.blend(Inventory, total=100)
        ing1 = mixer.blend(Ingredient, name=inv1, quantity=20.0)
        ing2 = mixer.blend(Ingredient, name=inv2, quantity=40.0)
        menu = mixer.blend(MenuItem, name='spaghetti', ingredients=ing1, price=5.25)
        new_fields = {'name': 'pasta', 'price': 10.25, 'ingredients': [ing1.pk, ing2.pk], 'status': 'available'}

        self.client.post(reverse_lazy('restaurant-menuitem-update', kwargs={'pk': menu.pk}), new_fields)

        menu.refresh_from_db()
        self.assertEqual(menu.name, 'pasta')
        self.assertEqual(menu.price, 10.25)
        self.assertEqual([i for i in menu.ingredients.all()], [ing1, ing2])
        self.assertEqual(menu.status, 'available')

    def test__invalid_status_update_to_available__db_entry_does_not_change_due_to_insufficient_inventory(self):
        inv = mixer.blend(Inventory, total=19)
        ing = mixer.blend(Ingredient, name=inv, quantity=20.0)
        menu = mixer.blend(MenuItem, ingredients=ing, author=self.staff_user, status='disabled')
        new_fields = {'name': menu.name, 'price': 12.0, 'ingredients': ing.pk, 'status': 'available'}

        response = self.client.post(reverse_lazy('restaurant-menuitem-update', kwargs={'pk': menu.pk}), new_fields)

        menu.refresh_from_db()
        self.assertEqual(menu.status, 'disabled')
        self.assertIn('Ingredient {} is insufficient'.format(ing.name.name),
                      response.context['form'].errors['__all__'])
