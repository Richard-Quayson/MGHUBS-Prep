from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Account
from .serializers import AccountRegistrationSerializer


class AccountRegistrationView(APIView):
    """
    view for creating a new user account
    """
    
    def post(self, request):
        serializer = AccountRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountLoginView(APIView):
    """
    view for logging in a user account
    """
    
    def post(self, request):
        pass