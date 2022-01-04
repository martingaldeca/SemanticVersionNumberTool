from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from core.models import Project


# This factory will create the 0.0.0 version associated because of the post_save signal
class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    name = FuzzyText()
    repository = 'https://github.com/'
