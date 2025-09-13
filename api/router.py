from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views.accounts import NoteViewSet, ProfileViewSet, UserRegistrationView, LogoutView
from api.views.accounts import PasswordResetRequestView, PasswordResetConfirmView

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/request/',PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/confirm/<uid>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]