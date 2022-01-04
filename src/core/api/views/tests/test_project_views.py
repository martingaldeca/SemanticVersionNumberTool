from random import randint

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.api.serializers import ProjectSerializer
from core.api.views.tests.mixins import APITestAuthenticatedMixin
from core.factories import ProjectFactory
from core.models import Project


class ProjectListViewTest(APITestAuthenticatedMixin, APITestCase):
    url = reverse('core:project_list')

    def test_get_200_OK(self):
        expected_results = []
        for i in range(randint(3, 10)):
            expected_results.append(ProjectSerializer(ProjectFactory()).data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], expected_results)


class CreateProjectViewTest(APITestAuthenticatedMixin, APITestCase):
    url = reverse('core:create_project')
    method = 'post'

    def setUp(self):
        super(CreateProjectViewTest, self).setUp()
        self.sent_data = {
            'name': 'test_project',
            'repository': 'https://github.com/',
        }

    def test_post_201_CREATED(self):
        response = self.client.post(self.url, data=self.sent_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            ProjectSerializer(
                instance=Project.objects.get(name=self.sent_data['name'])
            ).data
        )
