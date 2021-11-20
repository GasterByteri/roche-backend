from roche_api.models import users as user_models
from roche_api.models import journal as journal_models
from roche_api.serializers import UserSerializer, PatientSerializer, JournalSerializer, JournalDetailSerializer, TagSerializer
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

    def post(self, request, *args, **kwargs):
        file = request.data.pop('image')[0]
        journal_data = {
            "text_note" : request.data.get("text_note", ""),
            "image" : file,
        }
        created_by_id = int(request.data.get("created_by_id"))
        patient_id = int(request.data.get('patient_id'))
        created_by = user_models.User.objects.get(pk=created_by_id)
        patient = user_models.User.objects.get(pk=patient_id)

        journal = journal_models.Journal(**journal_data, patient=patient, created_by=created_by)
        journal.save()
        # serializer = JournalSerializer(journal)
        return Response({"id" : journal.id, "text_note" : journal.text_note, "image_url" : journal.image.name}, status=status.HTTP_200_OK)


class JournalDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = []
    permission_classes = []

    queryset = journal_models.Journal.objects.all()
    serializer_class = JournalDetailSerializer


class TagList(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = []

    queryset = journal_models.Tags.objects.all()
    serializer_class = TagSerializer


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = []
    permission_classes = []

    queryset = journal_models.Tags.objects.all()
    serializer_class = TagSerializer

