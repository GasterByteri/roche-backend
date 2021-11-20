from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from roche_api.models import users as user_models
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from roche_api.services.clients import chat as chat_client


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get("email")
        password = request.data.get("password")
        try:
            user = user_models.User.objects.get(username=username)
        except user_models.User.DoesNotExist:
            return Response({"message":"User with entered username does not exist!"}, status=status.HTTP_400_BAD_REQUEST)
        token = Token.objects.get(user=user).key

        if user.check_password(password):
            # If user is logged in, try to log in user to the chat app to obtain new credentials
            client = chat_client.ChatClient()

            chat_auth_token = client.login_user({
                "user" : username,
                "password": password,
            })

            return Response(
                {
                    "id": user.id,
                    "key": token,
                    "chat_key": chat_auth_token,
                }, status.HTTP_200_OK
            )
        return Response({"message":"Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_logout(request):
        user = user_models.User.objects.get(id=request.user.id)
        Token.objects.get(user=user).delete()
        logout(request)
        return Response({"message":"Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)