from roche_api.models import users as user_models
from roche_api.serializers import DoctorSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class DoctorList(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        doctors = user_models.Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)