from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from restaurant.views.sale_views import *
from restaurant.models import Sale


class TestPublicSaleViews(TestCase):

    def setUp(self):
        self.anon_user = mixer.blend(User)
        self.factory = RequestFactory()

    def test__sale_list__anyone_can_view(self):
        request = self.factory.get('/')
        request.user = self.anon_user
        response = SaleListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/sale/sale_list.html')

    def test__sale_details__anyone_can_view(self):
        ing = mixer.blend(Sale)
        request = self.factory.get('/')
        request.user = self.anon_user
        response = SaleDetailView.as_view()(request, pk=ing.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/sale/sale_detail.html')


class TestForbiddenSaleViews(TestCase):

    def setUp(self):
        self.anon_user = mixer.blend(User)
        self.staff = mixer.blend(User, is_staff=True)
        self.factory = RequestFactory()

    def test__update_sale__only_staff_can_view(self):
        ing = mixer.blend(Sale)
        request = self.factory.get('/')
        request.user = self.anon_user
        with self.assertRaises(PermissionDenied):
            SaleUpdateView.as_view()(request, pk=ing.pk)
        request.user = self.staff
        response = SaleUpdateView.as_view()(request, pk=ing.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/sale/sale_form.html')
