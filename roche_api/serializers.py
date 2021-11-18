import roche_api.models.users as user_models

from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_models.User
        fields = ['id', 'email', 'first_name', 'last_name', 'sex', 'role', 'is_admin', 'birth_date', 'phone_number']


class UserRegisterSerializer(RegisterSerializer):
    role = serializers.CharField(required=False)
    username = serializers.CharField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    sex = serializers.CharField(required=False)
    is_admin = serializers.BooleanField(required=False)
    birth_date = serializers.DateField(required=False)
    email = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    def save(self, request):
        print(request.POST.get("username"), request.POST.get("password"))
        user_mod = user_models.User(
            role=request.POST.get("role"),
            username=request.POST.get("username"),
            first_name=request.POST.get("first_name",''),
            last_name=request.POST.get("last_name",''),
            sex=request.POST.get("sex",'F'),
            is_admin=request.POST.get("is_admin",False),
            birth_date=request.POST.get("birth_date"),
            email=request.POST.get("email"),
            password=make_password(request.POST.get("password1")),
            )
        user_mod.save()
        return user_mod

