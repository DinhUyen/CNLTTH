from django.db import models
from django.contrib.auth.models import AbstractUser
from Common.generics import NO_ROLE
# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=255,unique=True)
    password= models.CharField(max_length=255)
    personID= models.CharField(max_length=20, blank=True, null=True)
    roleID = models.IntegerField(blank=True,default=NO_ROLE, null=True)
    userSetRole = models.CharField(max_length=255,blank=True,null=True)

    USERNAME_FIELD= 'username'
    REQUIRED_FIELDS=[]
    def __str__(self):
        return self.username