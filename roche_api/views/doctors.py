from roche_api.models import users as user_models
from roche_api.serializers import DoctorSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics


class DoctorList(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = []

    queryset = user_models.Doctor.objects.all()
    serializer_class = DoctorSerializer


class DoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = user_models.Doctor.objects.all()
    serializer_class = DoctorSerializer

# class DoctorList(APIView):
#     authentication_classes = []
#     permission_classes = []
#
#     def get(self, request, format=None):
#         doctors = user_models.Doctor.objects.all()
#         serializer = DoctorSerializer(doctors, many=True)
#         return Response(serializer.data)
#
#
# class DoctorDetail(APIView):
#     # Just for easier testing
#     authentication_classes = []
#     permission_classes = []
#
#     def get_object(self, pk):
#         try:
#             return user_models.Doctor.objects.get(pk=pk)
#         except user_models.Doctor.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         doctor = self.get_object(pk)
#         serializer = DoctorSerializer(doctor)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         doctor = self.get_object(pk)
#         serializer = DoctorSerializer(doctor, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         doctor = self.get_object(pk)
#         doctor.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
