from django.contrib.auth.models import User
from rest_framework import serializers
import re

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # Password validation: Ensures the password is at least 8 characters long
    def validate_password(self, value):
        # Check if password length is less than 8
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        # Check for password complexity: must include uppercase, lowercase, number, and special character
        if not all([
            re.search(r'[A-Z]', value),    # Uppercase letter
            re.search(r'[a-z]', value),    # Lowercase letter
            re.search(r'\d', value),        # Digit
            re.search(r'[!@#$%^&*(),.?":{}|<>]', value)  # Special character
        ]):
            raise serializers.ValidationError("Password must include an uppercase letter, lowercase letter, number, and special character.")
        
        # Block common weak patterns (e.g., "123", "password", etc.)
        if re.search(r'(123|abc|password|admin|\w)\1{2,}', value, re.IGNORECASE):
            raise serializers.ValidationError("Password contains a weak or easily guessable pattern.")
        
        return value
    
    # Username validation: Ensures the username is at least 5 characters long
    def validate_username(self, value):
        if len(value) <= 4:
            raise serializers.ValidationError("Username must be greater than 4 characters.")
        return value

    # Overriding the create method to hash the password before saving the user
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )

        return user
