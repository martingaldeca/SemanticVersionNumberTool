from django.contrib.auth.models import User
from rest_framework import status

from core.models import UserProfile


class CoreMixin:
    request = None
    context = None
    response_status_code = status.HTTP_201_CREATED

    @property
    def user(self) -> User:
        return self.request.user

    @property
    def profile(self) -> UserProfile:
        return self.request.user.profile

    def get_serializer_context(self):
        context = super(CoreMixin, self).get_serializer_context()
        context['user'] = self.user
        context['profile'] = self.profile
        return context
