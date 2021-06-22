from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from transitions.Project.models import Template
from transitions.Project.serializers.TemplateSerializers import TemplateGeneralSerializer


class TemplateView(APIView):
    def get(self, request, format=None):
        dataQ = Template.objects.all()
        serializer = TemplateGeneralSerializer(dataQ, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TemplateGeneralSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
