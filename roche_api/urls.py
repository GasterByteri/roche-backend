from django.urls import include, path
from . import views
from roche_api.views import users as user_views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
  # path('welcome', views.),
  path('users/', user_views.UserList.as_view()),
  path('users/<int:pk>/', user_views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)