import uuid
from random import choice

from django.contrib.auth.models import User
from django.test import TestCase

from core.api.serializers.version_serializers import (
    CreateNewVersionSerializer, UpdateVersionMajorSerializer,
    UpdateVersionMinorSerializer, UpdateVersionPatchSerializer,
    UpdateVersionSerializerMixin,
    VersionSerializerMixin
)
from core.exceptions import api as api_exceptions
from core.factories import ProjectFactory, UserFactory, VersionFactory
from core.models import Project, Version


class VersionSerializerMixinTest:
    used_serializer = VersionSerializerMixin

    class Meta:
        abstract = True

    def setUp(self):
        self.author: User = UserFactory()
        self.project: Project = ProjectFactory()
        self.sent_data = {
            'author': self.author.profile.uuid.hex,
            'project': self.project.uuid.hex
        }

    def test_author_not_found(self):
        self.sent_data['author'] = uuid.uuid4().hex
        with self.assertRaises(api_exceptions.NotFoundException) as validation_error:
            self.used_serializer(data=self.sent_data).is_valid(raise_exception=True)
        self.assertEqual(validation_error.exception.detail['message'], 'Not valid author')

    def test_project_not_found(self):
        self.sent_data['project'] = uuid.uuid4().hex
        with self.assertRaises(api_exceptions.NotFoundException) as validation_error:
            self.used_serializer(data=self.sent_data).is_valid(raise_exception=True)
        self.assertEqual(validation_error.exception.detail['message'], 'Not valid project')


class CreateNewVersionSerializerTest(VersionSerializerMixinTest, TestCase):
    used_serializer = CreateNewVersionSerializer

    def setUp(self):
        super(CreateNewVersionSerializerTest, self).setUp()
        self.sent_data.update(
            **{
                'major': 8,
                'minor': 8,
                'patch': 1994,
            }
        )

    def test_version_previously_created_conflict(self):
        previous_version: Version = VersionFactory()
        self.sent_data['project'] = previous_version.project.uuid.hex
        self.sent_data['major'] = previous_version.major
        self.sent_data['minor'] = previous_version.minor
        self.sent_data['patch'] = previous_version.patch
        with self.assertRaises(api_exceptions.ConflictException) as validation_error:
            CreateNewVersionSerializer(data=self.sent_data).is_valid(raise_exception=True)
        self.assertEqual(
            validation_error.exception.detail['message'], f'Version {previous_version} was previously created.'
        )

    def test_save(self):
        self.assertEqual(Version.objects.count(), 1)  # 1 project created with the factory, so version was 0.0.0 created
        serializer = CreateNewVersionSerializer(data=self.sent_data)
        serializer.is_valid(raise_exception=True)
        new_version = serializer.save()
        self.assertEqual(Version.objects.count(), 2)
        self.assertEqual(new_version.project.uuid.hex, self.sent_data['project'])
        self.assertEqual(new_version.author.profile.uuid.hex, self.sent_data['author'])
        self.assertEqual(new_version.major, self.sent_data['major'])
        self.assertEqual(new_version.minor, self.sent_data['minor'])
        self.assertEqual(new_version.patch, self.sent_data['patch'])

    def test_data(self):
        serializer = CreateNewVersionSerializer(data=self.sent_data)
        serializer.is_valid(raise_exception=True)
        self.assertEqual(serializer.data, 'Created')


class UpdateVersionSerializerMixinTest(VersionSerializerMixinTest):
    used_serializer = UpdateVersionSerializerMixin
    update_type = choice(
        [
            UpdateVersionMajorSerializer.update_type,
            UpdateVersionMinorSerializer.update_type,
            UpdateVersionPatchSerializer.update_type,
        ]
    )

    def setUp(self):
        super(UpdateVersionSerializerMixinTest, self).setUp()
        self.context = {'user': UserFactory()}

    def test_author_not_passed(self):
        self.assertEqual(Version.objects.count(), 1)
        self.sent_data.pop('author')
        serializer = self.used_serializer(data=self.sent_data, context=self.context)
        serializer.update_type = self.update_type
        serializer.is_valid(raise_exception=True)
        new_version = serializer.save()
        self.assertEqual(Version.objects.count(), 2)
        self.assertEqual(new_version.author, self.context['user'])

    def test_data(self):
        serializer = self.used_serializer(data=self.sent_data, context=self.context)
        serializer.update_type = self.update_type
        serializer.is_valid(raise_exception=True)
        self.assertEqual(serializer.data, str(Project.objects.get(uuid=self.sent_data['project'])))


class UpdateVersionMajorSerializerTest(UpdateVersionSerializerMixinTest, TestCase):
    used_serializer = UpdateVersionSerializerMixin
    update_type = UpdateVersionMajorSerializer.update_type

    def test_update_major(self):
        self.assertEqual(Version.objects.count(), 1)
        serializer = self.used_serializer(data=self.sent_data, context=self.context)
        serializer.update_type = self.update_type
        serializer.is_valid(raise_exception=True)
        new_version = serializer.save()
        self.assertEqual(Version.objects.count(), 2)
        self.assertEqual(new_version.major, 1)
        self.assertEqual(new_version.minor, 0)
        self.assertEqual(new_version.patch, 0)


class UpdateVersionMinorSerializerTest(UpdateVersionSerializerMixinTest, TestCase):
    used_serializer = UpdateVersionSerializerMixin
    update_type = UpdateVersionMinorSerializer.update_type

    def test_update_major(self):
        self.assertEqual(Version.objects.count(), 1)
        serializer = self.used_serializer(data=self.sent_data, context=self.context)
        serializer.update_type = self.update_type
        serializer.is_valid(raise_exception=True)
        new_version = serializer.save()
        self.assertEqual(Version.objects.count(), 2)
        self.assertEqual(new_version.major, 0)
        self.assertEqual(new_version.minor, 1)
        self.assertEqual(new_version.patch, 0)


class UpdateVersionPatchSerializerTest(UpdateVersionSerializerMixinTest, TestCase):
    used_serializer = UpdateVersionSerializerMixin
    update_type = UpdateVersionPatchSerializer.update_type

    def test_update_major(self):
        self.assertEqual(Version.objects.count(), 1)
        serializer = self.used_serializer(data=self.sent_data, context=self.context)
        serializer.update_type = self.update_type
        serializer.is_valid(raise_exception=True)
        new_version = serializer.save()
        self.assertEqual(Version.objects.count(), 2)
        self.assertEqual(new_version.major, 0)
        self.assertEqual(new_version.minor, 0)
        self.assertEqual(new_version.patch, 1)
