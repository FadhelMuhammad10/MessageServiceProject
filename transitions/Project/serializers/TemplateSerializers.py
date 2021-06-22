from rest_framework import serializers
from transitions.Project.models import Template


class TemplateGeneralSerializer(serializers.ModelSerializer):
    templates = serializers.CharField(allow_null=False,allow_blank=False)
    class Meta:
        model = Template
        exclude = []