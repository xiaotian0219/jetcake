from rest_framework import status, exceptions

from authentication.factories import UserFactory

from api.tests.mixins import BaseTestCase


class RegisterViewTestCase(BaseTestCase):
    def test_create_user(self):
        create_data = {
            'username': 'johndoe',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@email.com',
            'password': 'password',
        }
        res = self.client.post('/auth/register/', create_data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['user']['username'], create_data['username'])
        self.assertTrue('token' in res.data and 'user' in res.data)

        create_data = self.users[0]
        res = self.client.post('/auth/register/', create_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
