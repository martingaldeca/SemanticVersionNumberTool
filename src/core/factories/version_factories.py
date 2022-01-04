from factory import SubFactory
from factory.django import DjangoModelFactory

from core.factories import ProjectFactory, UserFactory
from core.models import Version


class VersionFactory(DjangoModelFactory):
    class Meta:
        model = Version

    project = SubFactory(ProjectFactory)
    patch = 8
    minor = 8
    major = 1994
    author = SubFactory(UserFactory)
