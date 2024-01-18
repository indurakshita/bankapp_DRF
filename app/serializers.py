
from rest_framework import serializers
from .models import UserProfile, Transaction

  


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
        
    
    



    

