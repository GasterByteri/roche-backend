from roche_api.services.clients import chat as chat_client
from rest_framework import status


def create_user_rocket_chat(user):
    client = chat_client.ChatClient()
    response = client.create_user(user)

    if response.status_code == status.HTTP_200_OK:
        print(f"User with id {user.id} is created in chatApp")
    else:
        print(f"User with id {user.id} is not created in chatApp")
