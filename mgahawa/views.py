from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from .serializer import *
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet


# Create your views here.
# class UserViewSet(viewsets.ModelViewSet):
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response({{'data': serializer.data}})

class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class RegisterUserViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserSerializer 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = request.data.get('email')
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')
        
        if not email or not password or not username:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Email, Username, or Password is required'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {
                    'status': status.HTTP_409_CONFLICT,
                    'message': 'Email Already Exists'
                },
                status=status.HTTP_409_CONFLICT
            )
            
        if User.objects.filter(username=username).exists():
            return Response(
                {
                    'status': status.HTTP_409_CONFLICT,
                    'message': "Username Already Exists"
                },
                status=status.HTTP_409_CONFLICT
            )
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        
        except Exception as e:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        return Response(
            {
                'status': status.HTTP_201_CREATED,
                'message': "User created successfully"
            },
            status=status.HTTP_201_CREATED
        )