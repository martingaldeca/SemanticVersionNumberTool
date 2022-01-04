from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from core.factories import UserFactory
from core.models import UserProfile


class UserProfileTest(TestCase):

    def setUp(self) -> None:
        self.user: User = UserFactory()
        self.profile: UserProfile = self.user.profile

    def test_user_creation_creates_user_profile(self):
        before_count = UserProfile.objects.count()
        UserFactory()
        self.assertEquals(UserProfile.objects.count(), before_count + 1)

    def test_user_profile_is_unique(self):
        self.assertRaises(IntegrityError, UserProfile.objects.create, user=self.user)
