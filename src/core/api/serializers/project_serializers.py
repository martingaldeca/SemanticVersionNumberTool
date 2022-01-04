from rest_framework import serializers

from core.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex')
    version = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['uuid', 'name', 'repository', 'version']

    def get_version(self, obj: Project):
        if obj.last_version:
            return obj.last_version.to_json()


class NewProjectSerializer(serializers.Serializer):
    name = serializers.CharField()
    repository = serializers.URLField(required=False)

    new_project = None

    def save(self, **kwargs):
        self.new_project = Project.objects.create(
            name=self.validated_data['name'],
            repository=self.validated_data['repository']
        )
        return self.new_project

    @property
    def data(self):
        return ProjectSerializer(instance=self.new_project).data
