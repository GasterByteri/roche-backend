from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from roche_api import constants as api_constants
from roche_api.models import users as user_models


class Journal(models.Model):
    class Meta:
        db_table = "journal"

    created_by = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    patient = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_owner"
    )
    text_note = models.TextField(null=False, blank=False)
    image_url = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
