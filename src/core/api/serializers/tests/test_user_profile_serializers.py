from django.test import TestCase

from core.api.serializers import UserProfileSerializer
from core.factories import UserProfileFactory
from core.models import UserProfile


class UserProfileSerializerTest(TestCase):

    def test_data(self):
        user_profile: UserProfile = UserProfileFactory()
        expected_data = {
            'uuid': user_profile.uuid.hex,
            'username': user_profile.user.username,
            'github': user_profile.github,
        }
        data = UserProfileSerializer(user_profile).data
        self.assertEqual(data, expected_data)
