from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.api import serializers
from core.mixins import CoreMixin


class VersionViewMixin(CoreMixin):
    permission_classes = (IsAuthenticated,)

    def post(self, request, project, *args, **kwargs):
        data = request.data
        data['project'] = project

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=self.response_status_code, headers=headers)


class CreateNewVersionView(VersionViewMixin, CreateAPIView):
    serializer_class = serializers.CreateNewVersionSerializer


class UpdateMajorView(VersionViewMixin, CreateAPIView):
    serializer_class = serializers.UpdateVersionMajorSerializer


class UpdateMinorView(VersionViewMixin, CreateAPIView):
    serializer_class = serializers.UpdateVersionMinorSerializer


class UpdatePatchView(VersionViewMixin, CreateAPIView):
    serializer_class = serializers.UpdateVersionPatchSerializer
