from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from mixer.backend.django import mixer
from restaurant.views.transaction_views import *
from restaurant.models import Transaction


class TestForbiddenTransactionViews(TestCase):

    def setUp(self):
        self.anon_user = mixer.blend(User)
        self.staff = mixer.blend(User, is_staff=True)
        self.factory = RequestFactory()

    def test__transaction_list__only_staff_can_view(self):
        request = self.factory.get('/')
        request.user = self.anon_user
        with self.assertRaises(PermissionDenied):
            TransactionListView.as_view()(request)
        request.user = self.staff
        response = TransactionListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/transaction/transaction_list.html')

    def test__transaction_details__only_staff_can_view(self):
        ing = mixer.blend(Transaction)
        request = self.factory.get('/')
        request.user = self.anon_user
        with self.assertRaises(PermissionDenied):
            TransactionDetailView.as_view()(request, pk=ing.pk)
        request.user = self.staff
        response = TransactionDetailView.as_view()(request, pk=ing.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/transaction/transaction_detail.html')

    def test__update_transaction__only_staff_can_view(self):
        ing = mixer.blend(Transaction)
        request = self.factory.get('/')
        request.user = self.anon_user
        with self.assertRaises(PermissionDenied):
            TransactionUpdateView.as_view()(request, pk=ing.pk)
        request.user = self.staff
        response = TransactionUpdateView.as_view()(request, pk=ing.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'restaurant/transaction/transaction_form.html')
