import re
from rest_framework import serializers
from .models import Account

EMAIL_REGEX = r"^[^0-9!@#$%^&*(+=)\\[\].></{}`]\w+([\.-_]?\w+)*@([a-z\d-]+)\.([a-z]{2,})(\.[a-z]{2,})?$"
PASSWORD_REGEX = r"^(?=(.*[A-Z]){2,})(?=(.*[a-z]){2,})(?=(.*\d){1,})(?=(.*[!#$%&()*+,-.:;<=>?@_~]){1,}).{8,}$"


class AccountRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True
    )
    confirm_password = serializers.CharField(
        write_only=True, 
        required=True
    )

    class Meta:
        model = Account
        fields = [
            "id", "firstname", "lastname", "email", "password", "confirm_password"
        ]
    
    def validate_firstname(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("First name must contain only letters")
        
        return value
    
    def validate_lastname(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Last name must contain only letters")
        
        return value
    
    def validate_email(self, value):
        if not re.match(EMAIL_REGEX, value):
            raise serializers.ValidationError("Invalid email address")
        
        if Account.objects.filter(email=value).exists():
            raise serializers.ValidationError("An account with this email already exists!")
        
        return value
    
    def validate_password(self, value):
        if not re.match(PASSWORD_REGEX, value):
            raise serializers.ValidationError("Invalid password. Password must contain at least 8 characters, 2 uppercase letters, 2 lowercase letters, 1 digit and 1 special character.")
        
        return value
    
    def validate_confirm_password(self, value):
        if not re.match(PASSWORD_REGEX, value):
            raise serializers.ValidationError("Invalid password. Password must contain at least 8 characters, 2 uppercase letters, 2 lowercase letters, 1 digit and 1 special character.")
        
        return value
    
    def create(self, **validated_data):      
        return Account.objects.create(**validated_data)
    
    def save(self):
        user_account = Account(
            firstname=self.validated_data["firstname"],
            lastname=self.validated_data["lastname"],
            email=self.validated_data["email"]
        )
        
        password = self.validated_data["password"]
        confirm_password = self.validated_data["confirm_password"]

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match!")
        else:
            user_account.set_password(password)
            user_account.save()
            return user_account