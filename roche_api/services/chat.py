from rocketchat.api import RocketChatAPI
import requests
import os
import environ

# Reading environment variables defined in .env
env = environ.Env()
environ.Env.read_env()

class ChatClient:
    api_host = 'http://23.88.57.2:3000'
    api_endpoint = os.path.join(api_host, "api/v1/")
    api_client = RocketChatAPI(settings={'username': env('ROCKET_CHAT_USERNAME'),'password': env('ROCKET_CHAT_PASS'),'domain': api_host})

    def create_user(self, user):
        chat_user_data = {
            'email' : user.email,
            'name': user.first_name,
            'pass': "randomPass",
            'username': user.username,
        }
        api_endpoint = os.path.join(self.api_endpoint, 'users.register')
        response = requests.post(api_endpoint, data=chat_user_data)
        return response

    def get_public_rooms(self):
        return self.api_client.get_public_rooms()