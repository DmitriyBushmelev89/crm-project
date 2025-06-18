from rest_framework.test import APITestCase
from rest_framework import status
from crm_app.models import Client


class ClientApiTest(APITestCase):
    def test_create_client_api(self):
        url = '/api/clients/'
        data = {
            'name': 'TestUser1',
            'email': 'testuser@test.com',
            'phone': '111'
        }
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(),1)
        client = Client.objects.first()
        self.assertEqual(client.email,'testuser@test.com')

    def test_create_client_api_neg(self):
        url = '/api/clients/'
        data = {
            'name': 'TestUser1',
            'email': 'testuser@test.com',
            'phone': '111'
        }
        response = self.client.post(url, data, format='json')

    def test_get_client_api(self):
        url = '/api/clients/'
        data = {
            'name': 'TestUser1',
            'email': 'testuser@test.com',
            'phone': '111'
        }
        response = self.client.post(url, data, format='json')
        ent_id = response.data['id']
        response = self.client.get(f'/api/clients/{ent_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'],'TestUser1')
        self.assertEqual(response.data['email'],'testuser@test.com')


