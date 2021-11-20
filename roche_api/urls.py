from django.urls import include, path
from . import views
from roche_api.views import users as user_views
from roche_api.views import patients as patient_views
from roche_api.views import doctors as doctor_views
from roche_api.views import chat as chat_views
from roche_api.views import authentication as authentication_views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
  path('login/', authentication_views.user_login),
  path('logout/', authentication_views.user_logout),
  path('users/', user_views.UserList.as_view()),
  path('users/<int:pk>/', user_views.UserDetail.as_view()),
  path('patients/', patient_views.PatientList.as_view()),
  path('patients/<int:pk>/', patient_views.PatientDetail.as_view()),
  path('doctors/', doctor_views.DoctorList.as_view()),
  path('doctors/<int:pk>/', doctor_views.DoctorDetail.as_view()),
  path('chat/', chat_views.chat_public_rooms),
  path('chat/private/', chat_views.chat_private_rooms),
  path('chat/<int:pk>', chat_views.chat_user),
]

urlpatterns = format_suffix_patterns(urlpatterns)

