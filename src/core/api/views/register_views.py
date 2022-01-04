from django.contrib.auth import get_user_model  # If used custom user model
from rest_framework.generics import CreateAPIView

from core.api import serializers


class RegisterView(CreateAPIView):
    model = get_user_model()
    serializer_class = serializers.RegisterSerializer
