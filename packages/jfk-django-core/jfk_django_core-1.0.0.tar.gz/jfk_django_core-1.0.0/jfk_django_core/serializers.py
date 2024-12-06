from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'is_superuser', 'permissions']

    def get_permissions(self, obj):
        return obj.get_all_permissions()