from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from transitions.Project.models import Log
from transitions.Project.serializers.LogSerializers import LogGeneralSerializer


class LogView(APIView):
    def get(self, request, format=None):
        dats = Log.objects.all()
        serializer = LogGeneralSerializer(dats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
