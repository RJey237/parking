from rest_framework.routers import SimpleRouter,DefaultRouter
user=DefaultRouter()
from .views import RegisterView,ProfileViewSet,CardViewSet
from django.urls import path, include

user.register(r"auth",RegisterView,basename="auth")
user.register(r"profile",ProfileViewSet,basename="profile")
user.register(r"card",CardViewSet,basename="card")


urlpatterns=[
    path('',include(user.urls)),
]