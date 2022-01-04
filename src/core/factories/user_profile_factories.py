import factory
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from factory import Faker, PostGenerationMethodCall, SubFactory
from factory.django import DjangoModelFactory

from core.models import UserProfile


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = Faker('user_name')
    password = PostGenerationMethodCall('set_password', 'adm1n')
    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    is_staff = False
    is_active = True
    is_superuser = False


# It's important to mute post_save signal, other case will create a collision when UserFactoryCreation
@factory.django.mute_signals(post_save)
class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = SubFactory(UserFactory)
    github = 'https://github.com/'
