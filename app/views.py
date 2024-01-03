from rest_framework import generics, permissions, status, viewsets
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .permissions import  IsOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView

from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from icecream import ic
from .models import UserProfile, Transaction
from .serializers import UserProfileSerializer,CustomLoginSerializer, UserRegistrationSerializer, TransactionSerializer
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


class CustomLoginView(APIView):
    serializer_class = CustomLoginSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/userprofile')  

        return Response({"detail": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def get(self, request):
        return render(request, 'logout.html')

    def post(self, request):
        logout(request)
        if not request.accepted_renderer.format == 'json':
            return redirect('login')
        return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
    

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def list(self, request, *args, **kwargs):
        user_profile = self.get_queryset().first()  
        transactions = user_profile.transactions.all()  
        context = {'user_profile': user_profile, 'transactions': transactions}
        return render(request, 'ac_detail.html', context)
    
class TransactionListCreateAPIView(ListCreateAPIView):
    serializer_class = TransactionSerializer
   
    def get_queryset(self):
        return Transaction.objects.filter(account__user=self.request.user)

    def perform_create(self, serializer):
        user_profile = UserProfile.objects.get(user=self.request.user)
        serializer.validated_data['account'] = user_profile
        transaction = serializer.save()
        account = transaction.account
        if transaction.transaction_type == 'deposit':
            account.balance += transaction.amount
        elif transaction.transaction_type == 'withdrawal':
            account.balance -= transaction.amount
        account.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            
            pass
        return response

# class TransactionViewSet(viewsets.ModelViewSet):
#     serializer_class = TransactionSerializer
#     permission_classes = [IsAuthenticated, IsOwner]

#     def get_queryset(self):
#         return Transaction.objects.filter(account__user=self.request.user)

#     def create(self, request, *args, **kwargs):
#         user_profile = UserProfile.objects.get(user=request.user)
#         serializer = TransactionSerializer(data=request.data)
        
#         if serializer.is_valid():
#             serializer.validated_data['account'] = user_profile
#             transaction = serializer.save()
#             account = transaction.account
            
#             if transaction.transaction_type == 'deposit':
#                 account.balance += transaction.amount
#             elif transaction.transaction_type == 'withdrawal':
#                 account.balance -= transaction.amount
            
#             account.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)