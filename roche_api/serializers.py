import roche_api.models.users as user_models
import roche_api.models.journal as journal_models

from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.hashers import make_password
from roche_api.services.data import users as user_data_service


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_models.User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'sex', 'role', 'birth_date', 'phone_number']


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

    def update(self, instance, validated_data):
        instance.user.username = validated_data.get("username", instance.user.username)
        instance.user.email = validated_data.get("email", instance.user.email)
        instance.user.first_name = validated_data.get("first_name", instance.user.first_name)
        instance.user.last_name = validated_data.get("last_name", instance.user.last_name)
        instance.user.sex = validated_data.get("sex", instance.user.sex)
        instance.user.birth_date = validated_data.get("birth_date", instance.user.birth_date)
        instance.user.phone_number = validated_data.get("phone_number", instance.user.phone_number)

        instance.municipality = validated_data.get("municipality", instance.municipality)
        instance.medical_record_number = validated_data.get("medical_record_number", instance.medical_record_number)
        instance.diagnosis = validated_data.get("diagnosis", instance.diagnosis)

        instance.save()

        return instance



# Doctor serializer
class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, required=False)
    patients = PatientSerializer(many=True, required=False)

    class Meta:
        model = user_models.Doctor
        fields = ['id', 'employee_number', 'department', 'title', 'room_number', 'hospital', 'city', 'user', 'patients']

    def update(self, instance, validated_data):
        instance.user.username = validated_data.get("username", instance.user.username)
        instance.user.email = validated_data.get("email", instance.user.email)
        instance.user.first_name = validated_data.get("first_name", instance.user.first_name)
        instance.user.last_name = validated_data.get("last_name", instance.user.last_name)
        instance.user.sex = validated_data.get("sex", instance.user.sex)
        instance.user.birth_date = validated_data.get("birth_date", instance.user.birth_date)
        instance.user.phone_number = validated_data.get("phone_number", instance.user.phone_number)

        instance.employee_number = validated_data.get("employee_number", instance.employee_number)
        instance.department = validated_data.get("department", instance.department)
        instance.title = validated_data.get("title", instance.title)
        instance.room_number = validated_data.get("room_number", instance.room_number)
        instance.hospital = validated_data.get("hospital", instance.hospital)
        instance.city = validated_data.get("city", instance.city)

        instance.save()

        return instance

class JournalDetailSerializer(serializers.ModelSerializer):
    created_by_id = serializers.IntegerField(required=True)
    patient_id = serializers.IntegerField(required=True)

    class Meta:
        model = journal_models.Journal
        fields = ['id', 'text_note', 'image', 'created_at', 'updated_at', 'patient_id', 'created_by_id']

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
        fields = ['id', 'text_note', 'image', 'created_at', 'updated_at', 'patient', 'created_by']


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = journal_models.Tags
        fields = ['id', 'name', 'color', 'icon']

class DoctorMembershipDetailSerializer(serializers.ModelSerializer):
    doctor_id = serializers.IntegerField(required=False)
    patient_id = serializers.IntegerField(required=False)
    mainDoctor = serializers.BooleanField(required=False)

    class Meta:
        model = user_models.PatientDoctorMembership
        fields = ['id', 'doctor_id', 'patient_id', 'mainDoctor']

    def create(self, validated_data):
        doctor_id = validated_data.pop("doctor_id")
        patient_id = validated_data.pop('patient_id')
        doctor = user_models.Doctor.objects.get(pk=doctor_id)
        patient = user_models.Patient.objects.get(pk=patient_id)
        membership = user_models.PatientDoctorMembership(**validated_data, doctor=doctor, patient=patient)
        return membership


class DoctorMembershipSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(many=False, required=False)
    patient = PatientSerializer(many=False, required=False)

    class Meta:
        model = user_models.PatientDoctorMembership
        fields = ['id', 'doctor', 'patient', 'mainDoctor']


