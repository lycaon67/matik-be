from rest_framework import serializers
from homes.models import *

class HomesSerializer(serializers.ModelSerializer):
    """
    Converts info querysets and model instance to native python data types.
    """
    class Meta:
        """Meta class"""
        model = Homes
        fields = '__all__'

class RoomsSerializer(serializers.ModelSerializer):
    """
    Converts info querysets and model instance to native python data types.
    """
    class Meta:
        """Meta class"""
        model = Rooms
        fields = '__all__'

class HomeUserSerializer(serializers.ModelSerializer):
    """
    Converts info querysets and model instance to native python data types.
    """
    class Meta:
        """Meta class"""
        model = HomeUserAccess
        fields = '__all__'
        