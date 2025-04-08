from rest_framework.viewsets import ViewSet,ModelViewSet
from .serializers import RegsterSerilaizer,VerifySerializer,UserProfileSerializer,CardSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action 
from .models import CustomUser,Card
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import  login


class RegisterView(ViewSet):
    @action(methods=['POST'],detail=False)
    def register(self,request):
        serializer=RegsterSerilaizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"user created"}, status=status.HTTP_200_OK)

    @action(methods=['POST'],detail=False)
    def verify_number(self,request):
        serializer=VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data=serializer.save()
        return Response(data)
    
    

class ProfileViewSet(ModelViewSet):
    queryset=CustomUser.objects.all()
    serializer_class=UserProfileSerializer 
    http_method_names=['get','patch','post']
    permission_classes=(IsAuthenticated,)

    
    def list(self, request, *args, **kwargs):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data)

class CardViewSet(ModelViewSet):
    # queryset=Card.objects.all()
    serializer_class=CardSerializer
    permission_classes=(IsAuthenticated,)

    
    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        data =serializer.save(user=self.request.user)
        return data

        # return super().perform_create(serializer);/.