import roche_api.models.users as user_models
import roche_api.models.journal as journal_models

from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.hashers import make_password
from roche_api.services.data import users as user_data_service


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_models.User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'sex', 'role', 'is_admin', 'birth_date', 'phone_number']


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_models.User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'sex', 'role', 'birth_date', 'phone_number']

# class UserRegisterSerializer(RegisterSerializer):
#     role = serializers.CharField(required=False)
#     username = serializers.CharField()
#     first_name = serializers.CharField(required=False)
#     last_name = serializers.CharField(required=False)
#     sex = serializers.CharField(required=False)
#     is_admin = serializers.BooleanField(required=False)
#     birth_date = serializers.DateField(required=False)
#     email = serializers.CharField(required=False)
#     password = serializers.CharField(required=False)
#
#     def save(self, request):
#         # Add here for specific user types
#         user_mod = user_models.User(
#             role=request.POST.get("role"),
#             username=request.POST.get("username"),
#             first_name=request.POST.get("first_name",''),
#             last_name=request.POST.get("last_name",''),
#             sex=request.POST.get("sex",'F'),
#             is_admin=request.POST.get("is_admin",False),
#             birth_date=request.POST.get("birth_date"),
#             email=request.POST.get("email"),
#             password=make_password(request.POST.get("password1")),
#             )
#         user_mod.save()
#
#         user_profile = user_data_service.create_user_profile(request.POST)
#         if user_profile:
#             user_profile.user = user_mod
#             user_profile.save()
#
#         return user_mod


# Patient serializer
class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, required=False)
    class Meta:
        model = user_models.Patient
        fields = ['id', 'municipality', 'medical_record_number', 'diagnosis', 'user']


# Doctor serializer
class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, required=False)
    patients = PatientSerializer(many=True, required=False)

    class Meta:
        model = user_models.Doctor
        fields = ['id', 'employee_number', 'department', 'title', 'room_number', 'hospital', 'city', 'user', 'patients']


class JournalDetailSerializer(serializers.ModelSerializer):
    created_by_id = serializers.IntegerField(required=True)
    patient_id = serializers.IntegerField(required=True)

    class Meta:
        model = journal_models.Journal
        fields = ['id', 'text_note', 'image_url', 'created_at', 'updated_at', 'patient_id', 'created_by_id']

    def create(self, validated_data):
        created_by_id = validated_data.get("created_by_id")
        patient_id = validated_data.pop('patient_id')
        created_by = user_models.User.objects.get(pk=created_by_id)
        patient = user_models.User.objects.get(pk=patient_id)
        journal = journal_models.Journal.objects.create(**validated_data, created_by=created_by, patient=patient)
        return journal

    def update(self, instance, validated_data):
        created_by_id = validated_data.get("created_by_id")
        patient_id = validated_data.pop('patient_id')
        created_by = user_models.User.objects.get_or_create(pk=created_by_id)
        patient = user_models.User.objects.get_or_create(pk=patient_id)

        instance.created_by = created_by
        instance.patient = patient

        instance.text_note = validated_data.get("text_note", instance.text_note)
        instance.image_url = validated_data.get("image_url", instance.image_url)

        instance.save()

        return instance

class JournalSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(many=False, required=True)
    patient = UserSerializer(many=False, required=True)

    class Meta:
        model = journal_models.Journal
        fields = ['id', 'text_note', 'image_url', 'created_at', 'updated_at', 'patient', 'created_by']
