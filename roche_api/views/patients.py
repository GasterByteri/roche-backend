from roche_api.models import users as user_models
from roche_api.serializers import UserSerializer, PatientSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from roche_api.services.data import users as users_data_service
from roche_api.services import chat as chat_service

class PatientList(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = []

    queryset = user_models.Patient.objects.all()
    serializer_class = PatientSerializer

    def post(self, request, *args, **kwargs):
        # try:

        user_data = request.data.pop("user")
        user = user_models.User.objects.create(**user_data)
        user.save()

        patient = user_models.Patient.objects.create(user=user, **request.data)
        patient.save()

        chat_service.create_user_rocket_chat(user, request.data.get("password"))

        # Create user in chatApp -- temporary here


        token, created = Token.objects.get_or_create(user=user)
        response_data = {
            "id": user.id,
            "key": token.key
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
        # except Exception as e:
        #     return Response({
        #         "message":e,
        #     }, status=status.HTTP_400_BAD_REQUEST)


class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = user_models.Patient.objects.all()
    serializer_class = PatientSerializer

# class PatientList(APIView):
#     authentication_classes = []
#     permission_classes = []
#
#     def get(self, request, format=None):
#         patients = user_models.Patient.objects.all()
#         serializer = PatientSerializer(patients, many=True)
#         return Response(serializer.data)


# class PatientDetail(APIView):
#     # Just for easier testing
#     authentication_classes = []
#     permission_classes = []

    # def get_object(self, pk):
    #     try:
    #         return user_models.Patient.objects.get(pk=pk)
    #     except user_models.Patient.DoesNotExist:
    #         raise Http404
    #
    # def get(self, request, pk, format=None):
    #     patient = self.get_object(pk)
    #     serializer = PatientSerializer(patient)
    #     return Response(serializer.data)
    #
    # def put(self, request, pk, format=None):
    #     patient = self.get_object(pk)
    #     serializer = PatientSerializer(patient, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, pk, format=None):
    #     patient = self.get_object(pk)
    #     patient.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
