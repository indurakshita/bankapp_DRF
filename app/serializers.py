# bankapp/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Transaction

  
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken. Please choose another one.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
 

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserProfile
        fields = ['username', 'account_number', 'balance']

class TransactionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='account.user.username', read_only=True)

    class Meta:
        model = Transaction
        fields = ['username', 'amount', 'transaction_type', 'timestamp']
        
    
    



    

