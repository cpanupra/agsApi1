from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class registerUser(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    def post(self,request,format=None):
        username=request.data['username']
        email=request.data['email']
        last_name = request.data['last_name']
        first_name = request.data['first_name']
        password = request.data['password']
        is_staff = request.data['is_staff']
        user=User.objects.create_user(username,email,password)
        user.is_staff=is_staff
        user.last_name=last_name
        user.first_name = first_name
        user.save()
        token=Token.objects.create(user=user)

        data={'detail': 'Usuario registrado con exito !!!!! con token : '+token.key}
        rpta=json.dumps(data)
        return HttpResponse(rpta,content_type='application/json')

class loginView(APIView):
    permission_classes = (AllowAny,)
    def post(self,request,format=None):
        username = request.data["username"]
        password = request.data["password"]
        #validar si el usuario existe en la base de datos
        user = authenticate(username=username,password=password)
        if user:
            token=Token.objects.get(user_id=user.id)
            data={
                'last_name': user.last_name,
                'first_name': user.first_name,
                'email': user.email,
                'token':token.key
            }
        else:
            data = {'detail':" usuario NO existe en la base de datos"}
        reply= json.dumps(data)
        return HttpResponse(reply,content_type='Application/json')
