from rest_framework import serializers


class UserProfileSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(format='hex')
    username = serializers.CharField(source='user.username')
    github = serializers.CharField()
