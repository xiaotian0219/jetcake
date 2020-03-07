from django.test import TestCase

from rest_framework.test import APIClient

from authentication.factories import UserFactory


class BaseTestCase(TestCase):
    def setUp(self):
        self.primary_user = UserFactory.create(**self.users[0])
        self.secondary_user = UserFactory.create(**self.users[1])

        self.client = APIClient()
        self.client.force_authenticate(self.primary_user)

        self.secondary_client = APIClient()
        self.secondary_client.force_authenticate(self.secondary_user)

    @property
    def users(self):
        return [
            {
                'username': 'admin',
                'first_name': 'admin',
                'last_name': 'admin',
                'email': 'admin@email.com',
                'password': 'password',
                'is_superuser': True,
            },
            {
                'username': 'test',
                'first_name': 'test',
                'last_name': 'test',
                'email': 'test@email.com',
                'password': 'password',
                'is_superuser': False,
            }
        ]
