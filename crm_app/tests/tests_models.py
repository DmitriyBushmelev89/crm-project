from django.test import TestCase
from crm_app.models import Client
from django.core.exceptions import ValidationError


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
