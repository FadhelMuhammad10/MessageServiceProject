from django.db import transaction
from rest_framework import serializers

from transitions.Project.models import CustomerEmail
from transitions.Project.serializers.AttachmentsSerializers import AttachmentSerializer


class CustomerEmailSendEmailGeneralSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(write_only=True, many=True)
    cc = serializers.ListField(write_only=True, child=serializers.CharField())
    email = serializers.ListField(write_only=True, child=serializers.CharField(), allow_empty=False)
    ccs = serializers.CharField(source="cc", read_only=True)
    emails = serializers.CharField(source="email", read_only=True)

    class Meta:
        model = CustomerEmail
        exclude = []

    @transaction.atomic()
    def create(self, validated_data):
        response = CustomerEmail.objects.create(**validated_data)
        return response
