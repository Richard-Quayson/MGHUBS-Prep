from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from django.utils import timezone

from .models import Account
from .serializers import AccountRegistrationSerializer, AccountLoginSerializer, AccountSerializer


class AccountRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        registers a new user
        """

        serializer = AccountRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            # use to_representation method to format the response
            return Response(AccountSerializer(account).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AccountLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AccountLoginSerializer(data=request.data)
        response = super().post(request, *args, **kwargs)
        
        if serializer.is_valid() and response.status_code == status.HTTP_200_OK:
            user = Account.objects.get(email=request.data["email"]) # type: ignore
            if not user.is_active:
                return Response({"error": "Account is disabled. Contact admin!"}, status=status.HTTP_400_BAD_REQUEST)
            
            response.set_cookie(
                key="refresh_token",
                value=response.data["refresh"], # type: ignore
                httponly=True,
                samesite="None",
                secure=True
            )
            response.set_cookie(
                key="access_token",
                value=response.data["access"], # type: ignore
                httponly=True,
                samesite="None",
                secure=True
            )

            # update user last login
            user.last_login = timezone.now()
            user.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return response
    

class AccountView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer

    def get(self, request):
        """
        returns the user account details
        """

        serializer = AccountSerializer(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AccountLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        logs out the user by blacklisting the refresh token
        and deleting the access and refresh tokens from the cookies
        """
        
        response = Response({"success": "User logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token")
        response.delete_cookie("access_token")
        return response