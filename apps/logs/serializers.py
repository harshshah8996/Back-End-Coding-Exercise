import json

from rest_framework import serializers
from .models import Log

class LogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Log
        fields = '__all__'


class GetLogSerializer(serializers.ModelSerializer):

    actionProperties = serializers.SerializerMethodField()

    def get_actionProperties(self, obj):
        return json.loads(obj.actionProperties)

    class Meta:
        model = Log
        fields = '__all__'