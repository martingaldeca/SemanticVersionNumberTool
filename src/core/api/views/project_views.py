from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from core.api import serializers
from core.models import Project


class ProjectListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProjectSerializer
    queryset = Project.objects.all()


class CreateProjectView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.NewProjectSerializer
