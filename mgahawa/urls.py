from django.urls import path, include
from . import views
from rest_framework import routers, serializers, viewsets
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'create_user', RegisterUserViewSet, basename='create_user')

urlpatterns = router.urls
