from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer,CustomTokenObtainPairSerializer,ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions,status,generics
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated  
from .models import User
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.tokens import BaseTokenGenerator
from Common import generics_cursor, custom_permission
from django.db import connection



class RegisterViewSet ( APIView ) :
    permission_classes = [permissions.AllowAny]

     # all swagger's parameters should be defined here   

    @swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, default='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, default='string'),
    }
    ))    

    @action(methods=['POST'], detail=False, url_path='registry-account')
    def post ( self , request ) :
        user=request.data["username"]        
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user=serializer.data['username']
        return Response(serializer.data ) 

class BlacklistRefreshViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='string')        
    }
    ))
    @action(methods=['POST'], detail=False, url_path='logout-account')

    def post(self, request):
        try:
            token = RefreshToken(request.data.get('refresh'))
            token.blacklist()
            return Response("Success")
        except:
            return Response("Token is invalid or expired", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MyTokenObtainPairViewSet(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ChangePasswordViewSet(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                return Response("Success.", status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetRoleViewSet ( APIView ) :
    permission_classes = [custom_permission.CustomPermissions]

    """
        API này dùng để lấy quyền truy cập ( roleID) của user hiện tại).
    """

    @swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, default='string'),
        'personID': openapi.Schema(type=openapi.TYPE_INTEGER, default=1),
        'roleID': openapi.Schema(type=openapi.TYPE_INTEGER, default=1),
    }
    ))    

    @action(methods=['POST'], detail=False, url_path='registry-account')
    def post ( self , request ) :
        user=request.data["username"]        
        roleID=request.data["roleID"]        
        personID=request.data["personID"]        
        userSetRole=request.user.username
        roleUserSetRole = request.user.roleID
        if roleID > roleUserSetRole:
            return Response(data={"status":False}, status=status.HTTP_200_OK)

        try:
            query_string = f'UPDATE Account_user SET roleID={roleID},personID={personID},userSetRole = "{userSetRole}" WHERE username = %s'
            param = [user]
            with connection.cursor() as cursor:
                cursor.execute(query_string, param)
                rows_affected = cursor.rowcount
            if rows_affected == 0:
                return Response(data={"status": False}, status=status.HTTP_200_OK)
        except:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"status":True}, status=status.HTTP_200_OK)
