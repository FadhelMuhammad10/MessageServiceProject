from django.contrib.auth.models import User
from django.db import transaction
from oauth2_provider.models import Application
from rest_framework import serializers, viewsets
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
class RegistrationSerializer(serializers.Serializer):
    @transaction.atomic()
    def create(self, validated_data):
       return User.objects.create_superuser(**validated_data)

class RegistrationViews(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    def create(self, request, *args, **kwargs):
        req = request.post('http://127.0.0.1:8000/oauth/')
        return None