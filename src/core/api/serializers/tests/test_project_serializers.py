from django.test import TestCase

from core.api.serializers import NewProjectSerializer, ProjectSerializer
from core.factories import ProjectFactory
from core.models import Project


class ProjectSerializerTest(TestCase):

    def test_data(self):
        project: Project = ProjectFactory()
        expected_data = {
            'uuid': project.uuid.hex,
            'name': project.name,
            'repository': project.repository,
            'version': project.last_version.to_json(),
        }
        data = ProjectSerializer(project).data
        self.assertEqual(data, expected_data)


class NewProjectSerializerTest(TestCase):

    def test_save(self):
        self.assertEqual(Project.objects.count(), 0)
        serializer_data = {
            'name': 'test',
            'repository': 'https://github.com/',
        }
        serializer = NewProjectSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        new_project = serializer.save()
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(new_project.name, serializer_data['name'])
        self.assertEqual(new_project.repository, serializer_data['repository'])

    def test_data(self):
        serializer_data = {
            'name': 'test',
            'repository': 'https://github.com/',
        }
        serializer = NewProjectSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        new_project = serializer.save()
        self.assertEqual(serializer.data, ProjectSerializer(new_project).data)
