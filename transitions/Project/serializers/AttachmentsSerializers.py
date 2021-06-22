from rest_framework import serializers


class AttachmentSerializer(serializers.Serializer):
    filebase64 = serializers.CharField()
    filename = serializers.CharField()