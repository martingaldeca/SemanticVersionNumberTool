from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user: User = None

    class Meta:
        model = User
        fields = ('username', 'password',)

    def save(self, **kwargs):
        self.user = User.objects.create_user(
            username=self.validated_data['username'],
            password=self.validated_data['password'],
        )
        return self.user

    @property
    def data(self):
        from core.api.serializers import UserProfileSerializer
        return UserProfileSerializer(self.user.profile).data
