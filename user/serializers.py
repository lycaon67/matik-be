from rest_framework import serializers
from user.models import *

class UserSerializer(serializers.ModelSerializer):
    """
    Converts info querysets and model instance to native python data types.
    """
    class Meta:
        """Meta class"""
        model = User
        fields = '__all__'

    # def create(self, validated_data):
    #     """Saves the data to the database and returns the instance of
    #         the created info.

    #     Args:
    #         - validated_data: info data

    #     Returns:
    #         - Info instance
    #     """
    #     return User.objects.create(**validated_data)