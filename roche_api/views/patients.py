from roche_api.models import users as user_models
from roche_api.serializers import UserSerializer, PatientSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class PatientList(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        patients = user_models.Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)