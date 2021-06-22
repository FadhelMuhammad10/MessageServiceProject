from django.db import transaction
from rest_framework import serializers

from transitions.Project.models import CustomerMessage, Template


class CustomerMessageSendSMSCheckSerializer(serializers.ModelSerializer):
    type_template = serializers.PrimaryKeyRelatedField(queryset=Template.objects.all(), write_only=True,
                                                       allow_null=False)
    text = serializers.ListField(write_only=True, child=serializers.CharField(), allow_empty=False)
    texts = serializers.CharField(read_only=True, source="text")

    class Meta:
        model = CustomerMessage
        exclude = ['kind']

    @transaction.atomic
    def create(self, validated_data):
        validated_data['kind'] = "SMS"
        response = CustomerMessage.objects.create(**validated_data)
        return response


class CustomerMessageSendWhatsappCheckSerializer(serializers.ModelSerializer):
    type_template = serializers.PrimaryKeyRelatedField(queryset=Template.objects.all(), write_only=True,
                                                       allow_null=False)
    text = serializers.ListField(write_only=True, child=serializers.CharField(), allow_empty=False)
    texts = serializers.CharField(source="text", read_only=True)

    class Meta:
        model = CustomerMessage
        exclude = ['kind']

    @transaction.atomic()
    def create(self, validated_data):
        validated_data['kind'] = "Whatsapp"
        response = CustomerMessage.objects.create(**validated_data)
        return response


class CustomerMessageSendWhatsapNoTemplateSerializer(serializers.ModelSerializer):
    text = serializers.CharField(allow_blank=False)

    class Meta:
        model = CustomerMessage
        exclude = ["kind", "type_template"]

    def create(self, validated_data):
        validated_data["kind"] = "Whatsapp"
        response = CustomerMessage.objects.create(**validated_data)
        return response


class CustomerMessageSendSMSNoTemplateSerializer(serializers.ModelSerializer):
    text = serializers.CharField(allow_blank=False)

    class Meta:
        model = CustomerMessage
        exclude = ["kind", "type_template"]

    def create(self, validated_data):
        validated_data["kind"] = "SMS"
        response = CustomerMessage.objects.create(**validated_data)
        return response
