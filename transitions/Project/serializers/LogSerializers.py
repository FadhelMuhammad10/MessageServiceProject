from rest_framework import serializers
from transitions.Project.models import Log


class LogGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        exclude = []