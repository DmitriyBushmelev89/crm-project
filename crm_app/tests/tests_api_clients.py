from rest_framework.test import APITestCase
from rest_framework import status
from crm_app.models import Client
from crm_app.models import Product
from crm_app.models import Order


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
        response = self.client.get(f'/api/clients/{ent_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'],'TestUser1')
        self.assertEqual(response.data['email'],'testuser@test.com')

    def test_update_client_api(self):
        url = '/api/clients/'
        data = {
            'name': 'TestUser1',
            'email': 'testuser@test.com',
            'phone': '111'
        }
        response = self.client.post(url, data, format='json')
        ent_id = response.data['id']
        data = {'name':'updated_value'}
        response = self.client.patch(f'/api/clients/{ent_id}/', data= data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'updated_value')

class ProductApiTest(APITestCase):
    def test_create_product(self):
        client = Client.objects.create(name='Client1', email='test@test.com', phone='123')
        url = '/api/products/'
        data = {
            'name': 'TestingProduct1',
            'price' : '9.50',
            'client': client.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        product = Product.objects.first()
        self.assertEqual(product.name, 'TestingProduct1')
        self.assertEqual(product.client.email, 'test@test.com')

    def test_get_product(self):
        client = Client.objects.create(name='Client1', email='test@test.com', phone='123')
        url = '/api/products/'
        data = {
            'name': 'TestingProduct1',
            'price': '9.50',
            'client': client.id
        }
        response = self.client.post(url, data, format='json')
        ent_id = response.data['id']
        response = self.client.get(f'/api/products/{ent_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'TestingProduct1')
        self.assertEqual(response.data['client'], 1)

    def test_update_product_api(self):
        client = Client.objects.create(name='Client1', email='test@test.com', phone='123')
        url = '/api/products/'
        data = {
            'name': 'TestingProduct_waiting_for_new_name',
            'price': '9.50',
            'client': client.id
        }
        response = self.client.post(url, data, format='json')
        ent_id = response.data['id']
        data = {'name': 'updated_value_for_product'}
        response = self.client.patch(f'/api/products/{ent_id}/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'updated_value_for_product')

    def test_get_destroy_product_api(self):
        client = Client.objects.create(name='Client1', email='test@test.com', phone='123')
        product = Product.objects.create(name = 'TestingProduct_for_delete', price=9.50, client = client)
        response = self.client.delete(f'/api/products/{product.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_price_less_than_10(self):
        client = Client.objects.create(name='Client1', email='test@test.com', phone='123')
        url = '/api/products/'
        data = {
            'name': 'TestingProduct1',
            'price': '0.99',
            'client': client.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Product.objects.count(), 0)

    def test_create_order(self):
        client = Client.objects.create(name='Client1', email='test@test.com', phone='123')
        product1 = Product.objects.create(name='Product A', price=12.00, client=client)
        product2 = Product.objects.create(name='Product B', price=15.00, client=client)
        url = '/api/orders/'
        data = {
            'client': client.id,
            "products": [product1.id, product2.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_price'], '27.00')
        self.assertEqual(len(response.data['products']),2 )

    def test_get_destroy_order_api(self):
        client = Client.objects.create(name='Client1', email='test@test.com', phone='123')
        product1 = Product.objects.create(name='Product A', price=12.00, client=client)
        product2 = Product.objects.create(name='Product B', price=15.00, client=client)
        url = '/api/orders/'
        data = {
            'client': client.id,
            "products": [product1.id, product2.id]
        }
        response = self.client.post(url, data, format='json')
        ent_id = response.data['id']
        response = self.client.get(f'/api/orders/{ent_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(),1)
        response = self.client.delete(f'/api/orders/{ent_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_with_incorrect_product(self):
        client = Client.objects.create(name='Client1', email='test@test.com', phone='123')
        product = Product.objects.create(name='Product A', price=12.00, client=client)
        url = '/api/orders/'
        data = {
            'client': client.id,
            "products": [product.id,99]
        }
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

