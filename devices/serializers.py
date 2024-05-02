from rest_framework import serializers
from devices.models import *


class DevicesSerializer(serializers.ModelSerializer):
    """
    Converts info querysets and model instance to native python data types.
    """
    class Meta:
        """Meta class"""
        model = Devices
        fields = '__all__'

class ChannelsSerializer(serializers.ModelSerializer):
    """
    Converts info querysets and model instance to native python data types.
    """
    class Meta:
        """Meta class"""
        model = Channels
        fields = '__all__'


        