from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from roche_api import constants as api_constants
from roche_api.models import users as user_models


def nameFile(instance, filename):
    return '/'.join(['images', filename])


class Journal(models.Model):
    class Meta:
        db_table = "journal"

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_owner",
        # primary_key=True
    )
    text_note = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=nameFile, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_access = models.ManyToManyField(
        user_models.User,
        related_name="Journal",
        through='UserJournalMembership',
        through_fields=('journal', 'user'),
    )


class UserJournalMembership(models.Model):
    class Meta:
        db_table = "user_journal"

    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)


class Tags(models.Model):
    class Meta:
        db_table = "tags"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    color = models.CharField(max_length=200, blank=True, null=True)
    icon = models.CharField(max_length=200, blank=True, null=True)
    journals = models.ManyToManyField(
        Journal,
        related_name="JournalTag",
        through='JournalTagMembership',
        through_fields=('tag', 'journal'),
    )


class JournalTagMembership(models.Model):
    class Meta:
        db_table = "journal_tag"
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)




