from django.test import TestCase
from crm_app.models import Client
from crm_app.models import Product
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.db.models import ProtectedError


class ClientModelTest(TestCase):
    def test_create_client(self):
        client = Client.objects.create(name='TestingUser1', email='test1@test.com', phone='111')
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(client.email, 'test1@test.com')
        self.assertEqual(client.name, 'TestingUser1')

    def test_create_client_wo_name(self):
        with self.assertRaises(ValidationError):
            client = Client(name='', email='test1@test.com', phone='111')
            client.full_clean()
            client.save()


class ProductModelTest(TestCase):

    def test_create_product(self):
        client = Client.objects.create(name='Testing Client_FK', email='test1@test.com', phone='111')
        product = Product.objects.create(
            name='Testing Product',
            price=Decimal('9.50'),
            client=client
        )
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(product.client.name, 'Testing Client_FK')

    def test_cannot_delete_client(self):
        client = Client.objects.create(name='Test_Client_for_deletion', email='test1@test.com', phone='111')
        product = Product.objects.create(
            name='Testing Product',
            price=Decimal('9.50'),
            client=client
        )
        with self.assertRaises(ProtectedError):
            client.delete()
