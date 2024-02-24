from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Account
import re


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
            "id", "firstname", "lastname", "email", "password", 
            "confirm_password", "last_login"
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
            raise serializers.ValidationError("Invalid password. Password must contain at least 2 uppercase letters, 2 lowercase letters, 1 digit and 1 special character. Minimum length is 8 characters.")
        
        return value
    
    def validate_confirm_password(self, value):
        if not re.match(PASSWORD_REGEX, value):
            raise serializers.ValidationError("Invalid password. Password must contain at least 2 uppercase letters, 2 lowercase letters, 1 digit and 1 special character. Minimum length is 8 characters.")
        
        return value

    def create(self, **validated_data):      
        return Account.objects.create(**validated_data)
    
    def save(self):
        user_account = Account(
            firstname=self.validated_data["firstname"],
            lastname=self.validated_data["lastname"],
            email=self.validated_data["email"],
        )
        
        password = self.validated_data["password"]
        confirm_password = self.validated_data["confirm_password"]

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match!")
        else:
            user_account.set_password(password)
            user_account.save()
            return user_account        


class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = [
            "id", "firstname", "lastname", "email", "last_login"
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["last_login"] = instance.last_login.strftime("%Y-%m-%d %H:%M:%S") if instance.last_login else None
        return data


class AccountLoginSerializer(TokenObtainPairSerializer):
    """
    defines a custom token obtain pair serializer which allows
    users to login with their email and password
    """
    
    email = serializers.EmailField(
        required=True,
        validators=[EMAIL_REGEX]
    )
    password = serializers.CharField(
        write_only=True, 
        required=True,
        trim_whitespace=False,
        label="Password",
        style={"input_type": "password"},
        validators=[PASSWORD_REGEX]
    )
    token = serializers.SerializerMethodField("get_token")

    class Meta:
        model = Account
        fields = ["email", "password", "token"]
        extra_kwargs = {
            "access": {"read_only": True},
            "refresh": {"read_only": True}
        }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # add user's firstname, lastname and role to token payload
        token["firstname"] = user.firstname
        token["lastname"] = user.lastname
        return token
    
    def validate_email(self, value):
        if re.match(EMAIL_REGEX, value):
            return value
        
        raise serializers.ValidationError("Invalid email address")
    
    def validate_password(self, value):
        if re.match(PASSWORD_REGEX, value):
            return value
        
        raise serializers.ValidationError("Password does not match required format. Password must contain at least 2 uppercase letters, 2 lowercase letters, 1 digit and 1 special character. Minimum length is 8 characters.")
    
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = Account.objects.get(email=email)
        if user is None:
            raise serializers.ValidationError("No user found with this email!")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password!")
        
        if not user.is_active:
            raise serializers.ValidationError("Account is disabled!")
        
        token = self.get_token(user)
        user_data = AccountSerializer(user).data
        user_data["refresh_token"] = str(token)
        user_data["access_token"] = str(token.access_token)
        return user_data