from roche_api.models import users as user_models
from roche_api.models import journal as journal_models
from roche_api.serializers import UserSerializer, PatientSerializer, JournalSerializer, JournalDetailSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from roche_api.services.data import users as users_data_service
from roche_api.services import chat as chat_service


class JournalList(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = []

    queryset = journal_models.Journal.objects.all()
    serializer_class = JournalDetailSerializer

    def get(self, request, *args, **kwargs):
        journals = journal_models.Journal.objects.all()
        serializer = JournalSerializer(journals, many=True)
        return Response(serializer.data)
