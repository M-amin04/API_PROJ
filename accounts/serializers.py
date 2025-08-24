from rest_framework import serializers
from accounts.models import User


class UserSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)