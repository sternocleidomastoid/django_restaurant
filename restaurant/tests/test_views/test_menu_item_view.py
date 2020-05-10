from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from mixer.backend.django import mixer
from restaurant.views.menu_item_views import *
from restaurant.models import MenuItem


class TestPublicMenuItemViews(TestCase):

    def setUp(self):
        self.anon_user = AnonymousUser
        self.factory = RequestFactory()

    def test__menu_item_list__anyone_can_view(self):
        request = self.factory.get('/')
        request.user = self.anon_user
        response = MenuItemListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/menu_item/menuitem_list.html')

    def test__menu_item_details__anyone_can_view(self):
        ing = mixer.blend(MenuItem)
        request = self.factory.get('/')
        request.user = self.anon_user
        response = MenuItemDetailView.as_view()(request, pk=ing.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/menu_item/menuitem_detail.html')


class TestForbiddenMenuItemViews(TestCase):

    def setUp(self):
        self.anon_user = mixer.blend(User)
        self.staff = mixer.blend(User, is_staff=True)
        self.factory = RequestFactory()

    def test__create_menu_item__only_staff_can_view(self):
        request = self.factory.get('/')
        request.user = self.anon_user
        with self.assertRaises(PermissionDenied):
            MenuItemCreateView.as_view()(request)
        request.user = self.staff
        response = MenuItemCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/menu_item/menuitem_form.html')

    def test__update_menu_item__only_staff_can_view(self):
        ing = mixer.blend(MenuItem)
        request = self.factory.get('/')
        request.user = self.anon_user
        with self.assertRaises(PermissionDenied):
            MenuItemUpdateView.as_view()(request, pk=ing.pk)
        request.user = self.staff
        response = MenuItemUpdateView.as_view()(request, pk=ing.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/menu_item/menuitem_form.html')

    def test__delete_menu_item__only_staff_can_view(self):
        ing = mixer.blend(MenuItem)
        request = self.factory.get('/')
        request.user = self.anon_user
        with self.assertRaises(PermissionDenied):
            MenuItemDeleteView.as_view()(request, pk=ing.pk)
        request.user = self.staff
        response = MenuItemDeleteView.as_view()(request, pk=ing.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/menu_item/menuitem_confirm_delete.html')
