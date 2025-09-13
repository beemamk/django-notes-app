from rest_framework import serializers
from accounts.models import Profile, Note
from django.contrib.auth.models import User

# This serializer is for the User model, for registration and login
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Profile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Create a profile for the new user
        Profile.objects.create(user=user)
        return user


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