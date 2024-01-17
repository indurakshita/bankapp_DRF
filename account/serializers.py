from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


  
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Username must contain at least 3 characters.")

        if not value.isalnum():
            raise serializers.ValidationError("Username must contain only alphanumeric characters.")

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
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials.")

        return data