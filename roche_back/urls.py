"""roche_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include('rest_auth.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('roche_api.urls')),
    # path('api/registration/', include('rest_auth.registration.urls')),
    path('api/docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'},
    ), name='swagger-ui'),

    path('api/openapi/', get_schema_view(
        title="Roche-hackaton",
        description="API schema",
        authentication_classes=[],
        permission_classes=[],
    ), name='openapi-schema'),
]
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
