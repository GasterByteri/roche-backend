from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from roche_api.models import users as user_models
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from roche_api.services.clients import chat as chat_client
from roche_api.services import questionnaire as questionaire_service


# SpreadSheet
# https://docs.google.com/spreadsheets/d/11pcfQqWT56OB-ibxg22m9kaYPlC5-Sdwca34gh8n0FA/edit?resourcekey#gid=1799916606
# Form
# https://docs.google.com/forms/d/1X0cRvoGE6D7ILdI6N8kM-dxkt5n9S1tFl4ZJT3fc550/edit

@api_view(['GET'])
@permission_classes([AllowAny])
def get_journal_entry(request):
    if request.method == 'GET':
        last_element = list(questionaire_service.get_last_entry_spreadsheet_symptoms())
        return Response(last_element[-1], status=status.HTTP_200_OK)
