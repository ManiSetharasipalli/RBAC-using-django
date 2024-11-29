from django.contrib.auth.models import User
from rest_framework import serializers
import re


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def validate_password(self, value):
        # Minimum length and complexity checks
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        # Comprehensive complexity validation
        if not all([
            re.search(r'[A-Z]', value),    # Uppercase
            re.search(r'[a-z]', value),    # Lowercase
            re.search(r'\d', value),        # Number
            re.search(r'[!@#$%^&*(),.?":{}|<>]', value)  # Special character
        ]):
            raise serializers.ValidationError("Password must include uppercase, lowercase, number, and special character.")
        
        # Block common weak patterns
        if re.search(r'(123|abc|password|admin|\w)\1{2,}', value, re.IGNORECASE):
            raise serializers.ValidationError("Password contains a weak or easily guessable pattern.")
        
        return value
    
    def validate_username(self, value):
        if len(value) <= 4:
            raise serializers.ValidationError("Username must be greater than 4 characters.")
        return value
        

    
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password']
        )

        return user
        
        