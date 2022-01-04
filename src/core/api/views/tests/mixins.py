from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from core.factories import UserFactory
from core.models import UserProfile


class APITestMixin:
    url = None
    method = 'get'

    def setUp(self) -> None:
        self.user: User = UserFactory(password='root1234')
        self.profile: UserProfile = self.user.profile
        self.client.login(username=self.user.username, password='root1234')
        response = self.client.post(
            reverse('token_obtain_pair'),
            {
                'username': self.user.username,
                'password': 'root1234'
            }
        )
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)


class APITestAuthenticatedMixin(APITestMixin):

    def test_not_authenticated_401_UNAUTHORIZED(self):
        self.client.logout()
        response = getattr(self.client, self.method)(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
