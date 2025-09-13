from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from accounts.models import Profile, Note
from api.serializers.accounts import ProfileSerializer, NoteSerializer
from django.shortcuts import get_object_or_404


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken



from rest_framework import generics
from api.serializers.accounts import UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "User registered successfully."},
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        #can view and update their own profile
        return Profile.objects.filter(user=self.request.user)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        profile = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'profile'):
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError("This user already has a profile.")


from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated


class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
        
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    filter_backends = [filters.SearchFilter]
    
    search_fields = ['title', 'description']




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from accounts.serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from accounts.utils import generate_reset_token, validate_reset_token
from rest_framework.permissions import AllowAny

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle] 
    throttle_scope = 'password_reset_request'

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = get_object_or_404(User, email__iexact=email)
            
            uid, token = generate_reset_token(user)
            
            reset_url = f"http://127.0.0.1:8000/reset-confirm/{uid}/{token}/"
            
            # Send email
            subject = 'Password Reset Request'
            message = f"""
            Click the link below to reset your password:
            {reset_url}
            
            This link expires in 1 hour. If you didn't request this, ignore it.
            """
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                return Response({'message': 'Reset link sent to your email.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': 'Failed to send email. Try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    throttle_scope = 'password_reset_confirm'

    def post(self, request, uid, token):
        user, db_token = validate_reset_token(uid, token)
        if not user or not db_token:
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                db_token.used = True
                db_token.save()
                
                return Response({'message': 'Password reset successful. Please log in.'}, status=status.HTTP_200_OK)
            except Exception:
                return Response({'error': 'Failed to update password.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)