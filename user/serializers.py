from rest_framework import serializers
from .models import User

class LoginSerializer(serializers.ModelSerializer):

    class Meta:
      model = User
      exclude=['created','updated']

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
      model = User
      exclude=['created','updated','authToken']

class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        include=['authToken',]

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    middle_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.CharField() 

    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
       
        return f"{obj['first_name']} {obj['last_name']}"

    