from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from roche_api import constants as api_constants


class User(AbstractUser):
    class Meta:
        db_table = "user"

    role = models.CharField(max_length=25, choices=api_constants.USER_TYPES, default=api_constants.PATIENT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    sex = models.CharField(max_length=1, choices=api_constants.OPTIONS_SEX, default='F', null=False)
    birth_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)


class Patient(models.Model):
    class Meta:
        db_table = "patient"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    # This can be connected with the google maps to search for a choice of cities -- can be done on the frontend
    municipality = models.CharField(max_length=100, blank=True, null=True)
    medical_record_number = models.CharField(max_length=100, null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        if self.user:
            self.user.delete()
        super().delete(*args, **kwargs)


class Doctor(models.Model):
    class Meta:
        db_table = "doctor"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    employee_number = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    room_number = models.CharField(max_length=100, blank=True, null=True)
    hospital = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    patients = models.ManyToManyField(
        Patient,
        related_name="doctors",
        through='PatientDoctorMembership',
        through_fields=('doctor', 'patient'),
    )

    def delete(self, *args, **kwargs):
        if self.user:
            self.user.delete()
        super().delete(*args, **kwargs)


class PatientDoctorMembership(models.Model):
    class Meta:
        db_table = "patient_doctor"

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    mainDoctor = models.BooleanField(default=True)
