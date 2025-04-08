from rest_framework import serializers
from .models import CustomUser,Card
from utils.exceptions import BaseAPIException
from django.contrib.auth import authenticate



class RegsterSerilaizer(serializers.ModelSerializer):
    password1=serializers.CharField(write_only=True, min_length=8)
    password2=serializers.CharField(write_only=True, min_length=8)


    class Meta:
        model =CustomUser
        fields =['username','password1', 'password2']

    def validate(self, data):
        if data['password1'] !=data['password2']:
            raise serializers.ValidationError({"password":"Passwords do not match"})
        return data
    
    def create(self, validated_data):
        user=CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1']
        )

        return user
    

class VerifySerializer(serializers.Serializer):
    user_id=serializers.IntegerField()
    code =serializers.IntegerField()

    
    def validate(self, data):
        user_id=data['user_id']
        if CustomUser.objects.filter(id=user_id).exists():
            raise serializers.ValidationError({"user not found"})
        return data
    
    def save(self, **kwargs):
        user_id=self.validated_data.get("user_id")
        code=self.validated_data.get("code")
        if code != 666666:
            raise BaseAPIException("code didn't match")


        user= CustomUser.objects.get(id=user_id)
        user.is_verified=True
        user.save()
        return{"message":"user activated"}
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =CustomUser
        fields=["first_name","last_name","user_type","phone","car_number","email_verified","is_verified"]


class CardSerializer(serializers.ModelSerializer):
    user=UserProfileSerializer(read_only=True)
    # first_name=serializers.CharField(source='user.first_name')
    class Meta:
        model=Card
        fields='__all__'
        read_only_field=['user']
        depth=1

