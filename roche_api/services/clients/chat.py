from rocketchat.api import RocketChatAPI
import requests
import os
import environ
from urllib.parse import urljoin
from rest_framework import status
import json


# Reading environment variables defined in .env
env = environ.Env()
environ.Env.read_env()

class ChatClient:
    api_host = 'http://23.88.57.2:3000'
    api_endpoint = urljoin(api_host, "api/v1/")
    api_client = RocketChatAPI(settings={'username': env('ROCKET_CHAT_USERNAME'),'password': env('ROCKET_CHAT_PASS'),'domain': api_host})

    def create_user(self, user, password):
        chat_user_data = {
            'email' : user.email,
            'name': user.first_name + " " + user.last_name,
            'pass': password,
            'username': user.username,
        }
        api_endpoint = urljoin(self.api_endpoint, 'users.register')
        response = requests.post(api_endpoint, data=chat_user_data)
        return response

    def get_public_rooms(self):
        return self.api_client.get_public_rooms()

    def get_private_rooms(self):
        return self.api_client.get_private_rooms()

    # Add members
    def create_public_room(self, room_name, members=[]):
        chat_data = {
            "name":room_name,
        }
        endpoint = urljoin(self.api_endpoint, 'channels.create')
        headers = {"X-Auth-Token": env('ROCKET_CHAT_AUTH_TOKEN'), "X-User-Id": env('ROCKET_CHAT_AUTH_ID')}
        response = requests.post(endpoint, data=chat_data, headers=headers)
        return response.json()

    def create_private_room(self, room_name, members=[]):
        chat_data = {
            "name": room_name,
            "members": members,
        }
        endpoint = urljoin(self.api_endpoint, 'groups.create')
        headers = {"X-Auth-Token": env('ROCKET_CHAT_AUTH_TOKEN'), "X-User-Id": env('ROCKET_CHAT_AUTH_ID')}
        response = requests.post(endpoint, json=chat_data, headers=headers)
        return response.json()

    def login_user(self, user_login_data):
        endpoint = urljoin(self.api_endpoint, 'login')
        response = requests.post(endpoint, data=user_login_data)
        if response.status_code == status.HTTP_200_OK:
            auth_token = response.json().get("data",{}).get("authToken")
            if auth_token:
                return auth_token
        else:
            return None
