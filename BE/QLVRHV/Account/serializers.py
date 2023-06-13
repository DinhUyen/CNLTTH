from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","password"]
        extra_kwargs = {
            'password' : { 'write_only' : True }
            }

    def create(self,validated_data) :
        password = validated_data.pop('password', None)
        instance = self.Meta.model ( ** validated_data )
        if password is not None :
            instance.set_password( password )
        instance.save()
        return instance
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # token['permission'] = user.roleID
        return token

class ChangePasswordSerializer(serializers.Serializer):

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

