from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import DestroyAPIView
from io import BytesIO
from django.core.mail import send_mail,EmailMessage
from .models import User, Attendance
from .serializers import UserSerializer,AttendanceSerializer

####### Aaccess ####### 
class LoginTokenObtainView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if hasattr(request.data, 'email'):
            if not User.objects.filter(email = request.data['email']).exists():
                return Response({"message": "Email Does Not Exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        tokens = serializer.validated_data

        # Serialize the user object
        user_serializer = UserSerializer(user)

        # Create the response data
        response_data = {
            'tokens': tokens,
            'user': user_serializer.data
        }

        return Response(response_data,status=status.HTTP_200_OK)


class LoginTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) # Reauest Data Have {refresh_token : ".."}

        try:
            serializer.is_valid(raise_exception=True)
        except:
            error_message = "Token is invalid or expired"
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)

        # user = serializer.user TokenRefreshSerializer -> Has no attribute user
        
        tokens = serializer.validated_data

        # Create the response data
        response_data = {
            'tokens': tokens, 
        }

        return Response(response_data)


class BlackListTokenView(APIView):
    # permission_classes = [AllowAny]

    def post(self,request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": e},status=status.HTTP_400_BAD_REQUEST)

class AttendanceListCreateAPIView(ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        user = self.request.user
        if user:
            if user.user_type == "ADMIN":
                return super().get_queryset()
            else:
                return Attendance.objects.filter(user=user)
            
        return Attendance.objects.none()
    