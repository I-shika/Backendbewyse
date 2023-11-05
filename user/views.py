from django.shortcuts import render
from .serializers import RegisterSerializer,LoginSerializer,TokenSerializer,ProfileSerializer
from .models import User
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.views import APIView
from firebase_admin import credentials, auth
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
def getusername():
    unique_id = User.objects.last()
    if unique_id:
        unique_value = unique_id.id + 1
    else:
        unique_value = 0
    return f"user{unique_value + 1}"

@api_view(['POST'])
def Register(request):
   data={}
   try:
     username=request.data.get("username")
     email= request.data.get("email")
     firstname= request.data.get("first_name")
     lastname= request.data.get("last_name")
     password=request.data.get("password")
     
       
     if username is not None and User.objects.filter(username=username).exists():
        return Response({"Faliure": "A user with that username already exists"}, status=status.HTTP_400_BAD_REQUEST)
     else:
         generated_username = getusername()
    #   def getusername(self, **kwargs):
    #         unique_id = User.objects.last()
    #         if unique_id:
    #             unique_value = unique_id.id + 1
    #         else:
    #          unique_value = 0
    #         return username + str((unique_value + 1) * 11)
    #         # self.data.username = user + \
    #         #     str((unique_value + 1) * 11)
      
    #         # return username

     print(generated_username)
     if  len(password)<8 :
        return Response({"Faliure": "This password is too short.It must contains atleast 8 characters"}, status=status.HTTP_400_BAD_REQUEST)

     if (not email or not password):
        return Response({"Faliure": "Email and password are required "}, status=status.HTTP_400_BAD_REQUEST)
     print(generated_username)
     if len(email)>100:
         return Response({"Faliure": "Only 100 characters are allowed for a field "}, status=status.HTTP_400_BAD_REQUEST)
     print("success")
     data = {
            "username": generated_username,
            "email": email,
            "firstname": firstname,
            "lastname": lastname,
            "password": password
        }
    #  print(data)
     db_entry = RegisterSerializer(data=data)   
     print("data")
     db_entry.is_valid(raise_exception=True)
     db_entry.save()
    
     return Response({"username": username}, status=status.HTTP_200_OK)
   except Exception as e:
    print(e)
    return Response({"Faliure": "dont know"}, status=status.HTTP_400_BAD_REQUEST)


       
@api_view(['POST'])
def Signin(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
                
        username = User.objects.filter(username=username).first()

        if email and User.check_password(password):
             cred = credentials.Certificate(settings.FIRBASE_CONFIG)
             auth_app = firebase_admin.initialize_app(cred)
            # authorization_header = request.META.get('HTTP_AUTHORIZATION')
             try:
               # Create a custom token
              custom_token = auth.create_custom_token(username,app=auth_app)
              print(custom_token)
             # Return the custom token in the response
              return Response({'custom_token': custom_token})
                # return Response({'success': 'Chemist login successful'}, status=status.HTTP_200_OK)    
             except:
                return Response({'failure': ''}, status=status.HTTP_401_UNAUTHORIZED)

    except:
         return Response({'failure': 'Username or password is invalid'}, status=status.HTTP_401_UNAUTHORIZED)
            
       

@api_view(['GET'])
def ViewProfile(request):
    if request.headers['Authorization']:
        id_token=request.headers['Authorization']
        try:
         # Verify the Firebase ID token
         decoded_token = auth.verify_id_token(id_token, app=firebase_app)

         # Extract user ID or other information from decoded_token
         user_id = decoded_token['uid']

         user = User.objects.filter(username=user_id)

         if not user:
           return Response({"error": "Invalid Auth Token"}, status=status.HTTP_401_BAD_REQUEST)
         else:

            data={
                'username': user.username,
                'email': user.email,
                'first_name': user.firstname,
                'last_name': user.lastname,

            }
        
         serializers = ProfileSerializer(user)
         serializedData = serializers.data

         return Response(serializedData)
        except:
                 return Response({'failure': 'Username or password is invalid'}, status=status.HTTP_401_UNAUTHORIZED)
@api_view(['POST'])
def EditProfile(request):
    if request.headers['Authorization']:
        id_token=request.headers['Authorization']
        try:
         # Verify the Firebase ID token
         decoded_token = auth.verify_id_token(id_token, app=firebase_app)

         # Extract user ID or other information from decoded_token
         user_id = decoded_token['uid']

         user = User.objects.filter(username=user_id)

         if not user:
           return Response({"error": "Invalid Auth Token"}, status=status.HTTP_401_BAD_REQUEST)
         else:
              username=request.data.get("username")
              firstname= request.data.get("first_name")
              lastname= request.data.get("last_name")
             
            
         if username is not None and User.objects.filter(username=username).exists():
          return Response({"Faliure": "A user with that username already exists"}, status=status.HTTP_400_BAD_REQUEST)
         data = {
            "username": generated_username,
            "firstname": firstname,
            "lastname": lastname,
            
         }
        #  print(data)
         db_entry = ProfileSerializer(data=data)   
         
         db_entry.is_valid(raise_exception=True)
         db_entry.save()

         return Response(serializedData)
        except:
                 return Response({'failure': 'Username or password is invalid'}, status=status.HTTP_401_UNAUTHORIZED)