from rest_framework import serializers
from .models import Profile, Note
from django.contrib.auth.models import User

# This serializer is for the User model, for registration and login
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# This serializer handles the user's profile data
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # Makes the user field read-only

    class Meta:
        model = Profile
        fields = ['id', 'user', 'full_name', 'dob', 'address', 'gender', 'mobile']
        # The 'user' field is read-only, preventing users from changing their associated User object.

# This serializer handles the Note model
class NoteSerializer(serializers.ModelSerializer):
    # 'owner' is a read-only field so it can be automatically assigned in the view
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Note
        fields = ['id', 'title', 'description', 'attachment', 'created_at', 'modified_at', 'owner']
        read_only_fields = ['created_at', 'modified_at']


        

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("No account found with this email.")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=8, write_only=True)
    re_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        if data['new_password'] != data['re_password']:
            raise serializers.ValidationError("Passwords do not match.")
        # Additional strength check (optional)
        if len(data['new_password']) < 8 or not any(c.isupper() for c in data['new_password']):
            raise serializers.ValidationError("Password must be at least 8 characters with one uppercase.")
        return data