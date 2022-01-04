from django.test import TestCase

from core.factories import ProjectFactory, VersionFactory
from core.models import Project, Version


class ProjectTest(TestCase):
    def setUp(self):
        self.project: Project = ProjectFactory()

    def test_last_version(self):
        self.assertEqual(self.project.last_version.formatted, '0.0.0')
        version: Version = VersionFactory(project=self.project)
        self.assertEqual(self.project.last_version, version)

    def test_create_first_version_on_created(self):
        self.assertEqual(Version.objects.count(), 1)
        project = ProjectFactory()
        self.assertEqual(Version.objects.count(), 2)
        project.name = 'test_name'
        project.save()
        self.assertEqual(Version.objects.count(), 2)
