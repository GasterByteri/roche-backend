from roche_api.models import users as user_models
from roche_api.serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from roche_api.services.data import users as user_data_service


class UserList(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = []

    queryset = user_models.User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        users = user_models.User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = user_models.User.objects.create(**request.data)
            user.set_password(request.data.get('password'))
            user.save()
            token,created = Token.objects.get_or_create(user=user)
            response_data = {
                "id": user.id,
                "key": token.key
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "message":e,
            }, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = user_models.User.objects.all()
    serializer_class = UserSerializer

# class UserList(APIView):
#     authentication_classes = []
#     permission_classes = []
#
#     def get(self, request, format=None):
#         users = user_models.User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)
#
#
# class UserDetail(APIView):
#     # Just for easier testing
#     authentication_classes = []
#     permission_classes = []
#
#     def get_object(self, pk):
#         try:
#             return user_models.User.objects.get(pk=pk)
#         except user_models.User.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         user = self.get_object(pk)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         user = self.get_object(pk)
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         user = self.get_object(pk)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
