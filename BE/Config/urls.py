from django.urls import include,path,re_path
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Swagger docs", # Standard
        default_version='v1.0', # Standard
        description="Swagger docs for HTTTQL", 
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path( r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', include("QLVRHV.Account.urls")),# Authen Services
    path('', include("QLVRHV.Address.urls")),# Address Services
    path('', include("QLVRHV.Person.urls")),# Person Services
]
