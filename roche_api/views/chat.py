from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from roche_api.models import users as user_models
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from roche_api.services import chat as chat_service

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def chat_public_rooms(request):
    chat_client = chat_service.ChatClient()
    if request.method == 'GET':
        public_rooms = chat_client.get_public_rooms()
        return Response(public_rooms, status=status.HTTP_200_OK)
    elif request.method == "POST":
        room_name = request.data.get("room_name")
        new_room = chat_client.create_public_room(room_name)
        return Response(new_room, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def chat_private_rooms(request):
    chat_client = chat_service.ChatClient()
    if request.method == 'GET':
        public_rooms = chat_client.get_private_rooms()
        return Response(public_rooms, status=status.HTTP_200_OK)
    elif request.method == "POST":
        room_name = request.data.get("room_name")
        new_room = chat_client.create_private_room(room_name)
        return Response(new_room, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def chat_user(request, pk):
    if request.method == 'POST':
        chat_client = chat_service.ChatClient()
        user = user_models.User.objects.get(pk=pk)
        response = chat_client.create_user(user)
        if response.status_code == status.HTTP_200_OK:
            return Response(response.json(), status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
