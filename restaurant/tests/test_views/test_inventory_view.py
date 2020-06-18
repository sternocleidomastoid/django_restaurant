from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from mixer.backend.django import mixer
from model_mommy import mommy

from restaurant.views.inventory_views import *
from restaurant.models import Inventory


class TestForbiddenInventoryViews(TestCase):

    def setUp(self):
        self.anon_user = mixer.blend(User)
        self.staff = mixer.blend(User, is_staff=True)
        self.factory = RequestFactory()

    def test__inventory_list__only_staff_can_view(self):
        request = self.factory.get('/')
        request.user = self.anon_user
        with self.assertRaises(PermissionDenied):
            InventoryListView.as_view()(request)
        request.user = self.staff
        response = InventoryListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/inventory/inventory_list.html')

    def test__inventory_details__only_staff_can_view(self):
        inv = mixer.blend(Inventory)
        request = self.factory.get('/')
        request.user = self.anon_user
        with self.assertRaises(PermissionDenied):
            InventoryDetailView.as_view()(request, pk=inv.pk)
        request.user = self.staff
        response = InventoryDetailView.as_view()(request, pk=inv.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/inventory/inventory_detail.html')

    def test__create_inventory__only_staff_can_view(self):
        request = self.factory.get('/')
        request.user = self.anon_user
        with self.assertRaises(PermissionDenied):
            InventoryCreateView.as_view()(request)
        request.user = self.staff
        response = InventoryCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/inventory/inventory_form.html')

    def test__update_inventory__only_staff_can_view(self):
        inv = mixer.blend(Inventory)
        request = self.factory.get('/')
        request.user = self.anon_user
        with self.assertRaises(PermissionDenied):
            InventoryUpdateView.as_view()(request, pk=inv.pk)
        request.user = self.staff
        response = InventoryUpdateView.as_view()(request, pk=inv.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/inventory/inventory_form.html')

    def test__delete_inventory__only_staff_can_view(self):
        inv = mixer.blend(Inventory)
        request = self.factory.get('/')
        request.user = self.anon_user
        with self.assertRaises(PermissionDenied):
            InventoryDeleteView.as_view()(request, pk=inv.pk)
        request.user = self.staff
        response = InventoryDeleteView.as_view()(request, pk=inv.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/inventory/inventory_confirm_delete.html')
        mommy.make(Inventory, name="PLEASE TEST THE SUCCESS URLS IN THE FUTURE")
