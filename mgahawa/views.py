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



class RegisterUserViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserSerializer 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = request.data.get('email')
        full_name = request.data.get('full_name')
        phone_number = request.data.get('phone_number')
        location = request.data.get('location')
        
        if not email or not full_name:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Your Details are required'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if UserProfile.objects.filter(email=email).exists():
            return Response(
                {
                    'status': status.HTTP_409_CONFLICT,
                    'message': 'Email Already Exists'
                },
                status=status.HTTP_409_CONFLICT
            )
            
        if UserProfile.objects.filter(full_name=full_name).exists():
            return Response(
                {
                    'status': status.HTTP_409_CONFLICT,
                    'message': "Username Already Exists"
                },
                status=status.HTTP_409_CONFLICT
            )
        
        try:
            user = UserProfile.objects.create_user(email=email)
            user.full_name = full_name
            user.phone_number = phone_number
            user.location = location
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

class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class CategorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True, is_deleted=False)
    serializer_class = CategorySerializer

class FoodItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FoodItem.objects.filter(is_active=True, is_deleted=False)
    serializer_class = FoodItemSerializer
    