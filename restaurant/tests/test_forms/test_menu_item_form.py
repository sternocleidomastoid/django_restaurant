from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from mixer.auto import mixer

from restaurant.models import MenuItem, Inventory, Ingredient


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


class TestMenuItemFormsUpdate(TestCase):

    def remove_keys_that_do_not_exist_in_db_keys(self, keys):
        for key in keys:
            self.new_fields.pop(key)

    def setUp(self):
        self.staff_user = mixer.blend(User, is_staff=True)
        self.staff_user.set_password('test123')
        self.staff_user.save()
        self.client.login(username=self.staff_user.username, password='test123')

    def test__valid_update__db_entry_changes_including_status_if_sufficient_inventory(self):
        self.inv = mixer.blend(Inventory, total=21)
        self.ing = mixer.blend(Ingredient, name=self.inv, quantity=20.0)
        self.menu = mixer.blend(MenuItem, ingredients=self.ing, author=self.staff_user, price=5.25, name='spaghetti')
        self.new_fields = {'name': 'pasta', 'price': 5.25, 'ingredients': self.ing.pk, 'status': 'available'}

        self.client.post(reverse_lazy('restaurant-menuitem-update', kwargs={'pk': self.menu.pk}), self.new_fields)

        self.remove_keys_that_do_not_exist_in_db_keys(['ingredients', 'price'])

        self.assertTrue(set(self.new_fields.items()).issubset(
            set(MenuItem.objects.get(pk=self.menu.pk).__dict__.items())))

    def test__invalid_status_update__db_entry_does_not_change_due_to_insufficient_inventory(self):
        self.inv = mixer.blend(Inventory, total=19)
        self.ing = mixer.blend(Ingredient, name=self.inv, quantity=20.0)
        self.menu = mixer.blend(MenuItem, ingredients=self.ing, author=self.staff_user)
        self.new_fields = {'name': self.menu.name, 'price': self.menu.price,
                           'ingredients': self.ing.pk, 'status': 'available'}

        response = self.client.post(reverse_lazy('restaurant-menuitem-update', kwargs={'pk': self.menu.pk}),
                                    self.new_fields)

        self.remove_keys_that_do_not_exist_in_db_keys(['ingredients', 'price', 'name'])

        self.assertFalse(set(self.new_fields.items()).issubset(
            set(MenuItem.objects.get(pk=self.menu.pk).__dict__.items())))
        self.assertEqual(response.status_code, 400)
