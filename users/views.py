from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework import status

from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import UserRegistrationSerializer, UserLoginSerializer

def home(request):
    return HttpResponse("Hello World")

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                token_key = Token.objects.get_or_create(user=user).key
                return Response({
                    'token_key': token_key
                })
            else:
                return Response({
                    'message': 'Invalid username or password.'
                })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
