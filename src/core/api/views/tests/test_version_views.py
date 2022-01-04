from unittest import mock

from django.contrib.auth.models import User
from django.http import QueryDict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.api.serializers import CreateNewVersionSerializer, UpdateVersionMajorSerializer, UpdateVersionMinorSerializer, \
    UpdateVersionPatchSerializer
from core.api.views.tests.mixins import APITestAuthenticatedMixin
from core.factories import ProjectFactory, UserFactory
from core.models import Project, Version


class VersionViewMixinTest:

    def setUp(self):
        super(VersionViewMixinTest, self).setUp()
        self.project: Project = ProjectFactory()
        self.author: User = UserFactory()
        self.sent_data = self.serializer_data = {
            'author': self.author.profile.uuid.hex,
        }
        self.serializer_data.update(**{'project': self.project.uuid.hex})
        self.url = None
        self.serializer = None


class CreateNewVersionViewTest(VersionViewMixinTest, APITestAuthenticatedMixin, APITestCase):
    method = 'post'

    def setUp(self):
        super(CreateNewVersionViewTest, self).setUp()
        self.url = reverse('core:new_version', kwargs={'project': self.project.uuid.hex})
        self.serializer = CreateNewVersionSerializer
        self.sent_data.update(
            **{
                'major': 8,
                'minor': 8,
                'patch': 1994,
            }
        )

    def test_post_201_CREATED(self):
        self.assertEqual(Version.objects.count(), 1)  # 1 project created with the factory, so version was 0.0.0 created
        with mock.patch.object(
            QueryDict, '_mutable', new_callable=mock.PropertyMock
        ) as mock_mutable:  # Must mock for test QueryDict objects
            mock_mutable.return_value = True
            response = self.client.post(self.url, data=self.sent_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 'Created')
        self.assertEqual(Version.objects.count(), 2)


class UpdateVersionViewMixin:

    def test_post_201_CREATED(self):
        self.assertEqual(Version.objects.count(), 1)  # 1 project created with the factory, so version was 0.0.0 created
        with mock.patch.object(
            QueryDict, '_mutable', new_callable=mock.PropertyMock
        ) as mock_mutable:  # Must mock for test QueryDict objects
            mock_mutable.return_value = True
            response = self.client.post(self.url, data=self.sent_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        serializer = self.serializer(data=self.serializer_data)
        serializer.is_valid(raise_exception=True)
        expected_data = serializer.data
        self.assertEqual(response.data, expected_data)
        self.assertEqual(Version.objects.count(), 2)


class UpdateMajorViewTest(UpdateVersionViewMixin, VersionViewMixinTest, APITestAuthenticatedMixin, APITestCase):
    method = 'post'

    def setUp(self):
        super(UpdateMajorViewTest, self).setUp()
        self.url = reverse('core:update_major', kwargs={'project': self.project.uuid.hex})
        self.serializer = UpdateVersionMajorSerializer


class UpdateMinorViewTest(UpdateVersionViewMixin, VersionViewMixinTest, APITestAuthenticatedMixin, APITestCase):
    method = 'post'

    def setUp(self):
        super(UpdateMinorViewTest, self).setUp()
        self.url = reverse('core:update_minor', kwargs={'project': self.project.uuid.hex})
        self.serializer = UpdateVersionMinorSerializer


class UpdatePatchViewTest(UpdateVersionViewMixin, VersionViewMixinTest, APITestAuthenticatedMixin, APITestCase):
    method = 'post'

    def setUp(self):
        super(UpdatePatchViewTest, self).setUp()
        self.url = reverse('core:update_patch', kwargs={'project': self.project.uuid.hex})
        self.serializer = UpdateVersionPatchSerializer
