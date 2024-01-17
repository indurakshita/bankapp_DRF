from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from app.models import UserProfile
from .serializers import  UserRegistrationSerializer
import random



class SignupView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        account_number = self.generate_account_number(user.username)
        UserProfile.objects.create(user=user, account_number=account_number)
        return redirect('login')

    def generate_account_number(self, username):
        username_prefix = username[:2].upper()
        random_number = str(random.randint(10000, 99999))
        return f"{username_prefix}{random_number}"


def generate_token_for_user(user):
    existing_token = Token.objects.filter(user=user).first()
    if existing_token:   
        return existing_token
    else:    
        return Token.objects.create(user=user)

class CustomLoginView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        if request.user.is_authenticated:
           
            return redirect('/api/userprofile/')
        else:
            
            return render(request, 'login.html')
        
        
    def post(self, request):
        token = request.data.get('token')
        if token:
            try:
                user = Token.objects.get(key=token).user
                login(request, user)
                return Response({"detail": "Login successful"}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({"detail": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                token = generate_token_for_user(user)
                login(request, user)
                return redirect('/api/userprofile/')
                
            else:
                return Response({"detail": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def get(self, request):
        return render(request, 'logout.html')

    def post(self, request):
        logout(request)
        if not request.accepted_renderer.format == 'json':
            return redirect('login')
        return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)