from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import *


urlpatterns = [
    path('authenticator/register/', RegisterViewSet.as_view(), name='registry'),
    path('authenticator/login/', MyTokenObtainPairViewSet.as_view(), name='login'),
    path('authenticator/changePassword/', ChangePasswordViewSet.as_view(), name='change_password'),
    path('authenticator/refreshToken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('authenticator/logout', BlacklistRefreshViewSet.as_view(), name="logout"),
    path('account/setRoleUser', SetRoleViewSet.as_view(), name="set_role_user"),
   
]