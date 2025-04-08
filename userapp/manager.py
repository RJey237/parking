from django.db import models
from django.contrib.auth.models import BaseUserManager 


class AdminManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type='admin')

class DriverManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type='driver')

class OwnerManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type='owner')
