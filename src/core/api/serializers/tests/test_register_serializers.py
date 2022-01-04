from django.contrib.auth.models import User
from django.test import TestCase

from core.api.serializers import RegisterSerializer, UserProfileSerializer


class RegisterSerializerTest(TestCase):

    def setUp(self):
        super(RegisterSerializerTest, self).setUp()
        self.serialized_data = {
            'username': 'foo',
            'password': 'root1234',
        }

    def test_create(self):
        self.assertEqual(User.objects.count(), 0)
        serializer = RegisterSerializer(data=self.serialized_data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(new_user.username, self.serialized_data['username'])
        self.assertTrue(new_user.check_password(self.serialized_data['password']))

    def test_data(self):
        serializer = RegisterSerializer(data=self.serialized_data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.save()
        self.assertEqual(serializer.data, UserProfileSerializer(new_user.profile).data)
