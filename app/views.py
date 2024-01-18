from rest_framework import  status, viewsets
from .permissions import  IsOwner
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework import viewsets
from django.shortcuts import render,redirect 
from rest_framework.response import Response
from django.urls import reverse
from .models import UserProfile, Transaction
from .serializers import UserProfileSerializer, TransactionSerializer



class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.filter(user=request.user).first()  
        
        
        if user_profile:
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
            return redirect("/api/userprofile/")

