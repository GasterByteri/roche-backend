from roche_api.services.clients import chat as chat_client
from rest_framework import status
from roche_api import constants
from roche_api.models import users

def create_user_rocket_chat(user, password):
    client = chat_client.ChatClient()
    response = client.create_user(user, password)
    chat_user_name = user.first_name + '_' + user.last_name
    if user.role == constants.PATIENT:
        private_group_user_doctor = client.create_private_room(chat_user_name,members=[user.username])
    # elif user.role == constants.DOCTOR:
    #     all_patients = users.PatientDoctorMembership.objects.filter(doctor=user)




    if response.status_code == status.HTTP_200_OK:
        print(f"User with id {user.id} is created in chatApp")
    else:
        print(f"User with id {user.id} is not created in chatApp")
