from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.api.serializers import UserProfileSerializer
from core.api.views.tests.mixins import APITestMixin
from core.factories import UserFactory


class RegisterViewTest(APITestMixin, APITestCase):
    url = reverse('core:register')
    method = 'post'

    def setUp(self):
        super(RegisterViewTest, self).setUp()
        self.sent_data = {
            'username': 'foo',
            'password': 'root1234',
        }

    def test_post_username_previously_registered_400_BAD_REQUEST(self):
        UserFactory(username=self.sent_data['username'])
        response = self.client.post(self.url, data=self.sent_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_201_CREATED(self):
        response = self.client.post(self.url, data=self.sent_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            UserProfileSerializer(User.objects.get(username=self.sent_data['username']).profile).data
        )
