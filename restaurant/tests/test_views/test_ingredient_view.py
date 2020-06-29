from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from mixer.backend.django import mixer
from restaurant.views.ingredient_views import *
from restaurant.models import Ingredient


class TestForbiddenIngredientViews(TestCase):

    def setUp(self):
        self.anon_user = mixer.blend(User)
        self.staff = mixer.blend(User, is_staff=True)
        self.factory = RequestFactory()

    def test__ingredient_list__only_staff_can_view(self):
        request = self.factory.get('/')
        request.user = self.anon_user
        with self.assertRaises(PermissionDenied):
            IngredientListView.as_view()(request)
        request.user = self.staff
        response = IngredientListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/ingredient/ingredient_list.html')

    def test__ingredient_details__only_staff_can_view(self):
        ing = mixer.blend(Ingredient)
        request = self.factory.get('/')
        request.user = self.anon_user
        with self.assertRaises(PermissionDenied):
            IngredientDetailView.as_view()(request, pk=ing.pk)
        request.user = self.staff
        response = IngredientDetailView.as_view()(request, pk=ing.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/ingredient/ingredient_detail.html')

    def test__create_ingredient__only_staff_can_view(self):
        request = self.factory.get('/')
        request.user = self.anon_user
        with self.assertRaises(PermissionDenied):
            IngredientCreateView.as_view()(request)
        request.user = self.staff
        response = IngredientCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/ingredient/ingredient_form.html')

    def test__update_ingredient__only_staff_can_view(self):
        ing = mixer.blend(Ingredient)
        request = self.factory.get('/')
        request.user = self.anon_user
        with self.assertRaises(PermissionDenied):
            IngredientUpdateView.as_view()(request, pk=ing.pk)
        request.user = self.staff
        response = IngredientUpdateView.as_view()(request, pk=ing.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/ingredient/ingredient_form.html')

    def test__delete_ingredient__only_staff_can_view(self):
        ing = mixer.blend(Ingredient)
        request = self.factory.get('/')
        request.user = self.anon_user
        with self.assertRaises(PermissionDenied):
            IngredientDeleteView.as_view()(request, pk=ing.pk)
        request.user = self.staff
        response = IngredientDeleteView.as_view()(request, pk=ing.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/ingredient/ingredient_confirm_delete.html')
