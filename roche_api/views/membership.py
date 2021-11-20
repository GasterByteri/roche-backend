from roche_api.models import users as user_models
from roche_api.models import journal as journal_models
from roche_api.serializers import UserSerializer, DoctorMembershipSerializer, DoctorMembershipDetailSerializer, JournalSerializer, JournalDetailSerializer, TagSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from roche_api.services.data import users as users_data_service
from roche_api.services import chat as chat_service

class MembershipList(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = []

    queryset = user_models.PatientDoctorMembership.objects.all()
    serializer_class = DoctorMembershipDetailSerializer

    def get(self, request, *args, **kwargs):
        memberships = user_models.PatientDoctorMembership.objects.all()
        serializer = DoctorMembershipSerializer(memberships, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        membership_data = {
            "mainDoctor" : request.data.get("mainDoctor", True),
        }
        doctor_id = int(request.data.get("doctor_id"))
        patient_id = int(request.data.get('patient_id'))
        doctor = user_models.Doctor.objects.get(pk=doctor_id)
        patient = user_models.Patient.objects.get(pk=patient_id)

        membership = user_models.PatientDoctorMembership(**membership_data, patient=patient, doctor=doctor)
        membership.save()
        # serializer = JournalSerializer(journal)
        return Response({"id" : membership.id, "doctor_id" : membership.doctor.id, "patient_id" : membership.patient.id, "mainDoctor":membership.mainDoctor}, status=status.HTTP_200_OK)



class MembershipDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = []
    permission_classes = []

    queryset = user_models.PatientDoctorMembership.objects.all()
    serializer_class = DoctorMembershipDetailSerializer