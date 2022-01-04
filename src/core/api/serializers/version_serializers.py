from django.contrib.auth.models import User
from rest_framework import serializers

from core.exceptions import api as api_exceptions
from core.models import Project, UserProfile, Version


class VersionSerializerMixin(serializers.Serializer):
    project = serializers.UUIDField()
    author = serializers.UUIDField(required=False)

    def validate_author(self, value):
        if user_profile_qs := UserProfile.objects.filter(uuid=value):
            return user_profile_qs.last().user
        raise api_exceptions.NotFoundException('Not valid author')

    @staticmethod
    def validate_project(value):
        if project_qs := Project.objects.filter(uuid=value):
            return project_qs.last()
        raise api_exceptions.NotFoundException('Not valid project')


class CreateNewVersionSerializer(VersionSerializerMixin):
    major = serializers.IntegerField()
    minor = serializers.IntegerField()
    patch = serializers.IntegerField()

    def is_valid(self, raise_exception=False):
        validation = super().is_valid(raise_exception=True)
        if version_qs := Version.objects.filter(
            project=self.validated_data.get('project'),
            major=self.validated_data.get('major'),
            minor=self.validated_data.get('minor'),
            patch=self.validated_data.get('patch'),
        ):
            raise api_exceptions.ConflictException(f'Version {version_qs.last()} was previously created.')
        return validation

    def save(self, **kwargs):
        return Version.objects.create(
            project=self.validated_data.get('project'),
            author=self.validated_data.get('author'),
            major=self.validated_data.get('major'),
            minor=self.validated_data.get('minor'),
            patch=self.validated_data.get('patch'),
        )

    @property
    def data(self):
        return 'Created'


class UpdateVersionSerializerMixin(VersionSerializerMixin):
    update_type = None
    new_version = None

    class Meta:
        abstract = True

    def save(self, **kwargs):
        project: Project = self.validated_data['project']
        author: User = self.validated_data.get('author', self.context['user'])
        last_version: Version = project.last_version
        self.new_version = last_version.next_version(update_type=self.update_type, author=author)
        return self.new_version

    @property
    def data(self):
        return str(self.validated_data['project'])


class UpdateVersionMajorSerializer(UpdateVersionSerializerMixin):
    update_type = 'major'


class UpdateVersionMinorSerializer(UpdateVersionSerializerMixin):
    update_type = 'minor'


class UpdateVersionPatchSerializer(UpdateVersionSerializerMixin):
    update_type = 'patch'
