from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from authapp import models


class LoginUserSerializer(serializers.Serializer):
    """ Authentication SignIn Serializer """
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    
    def get_user(self, is_active=False):
        if 'email' in self.data and 'password' in self.data:
            try:
                user = models.User.objects.get(
                    is_active=is_active,
                    email=self.data.get('email')
                )
                if user.has_usable_password():
                    return user
            except models.User.DoesNotExist:
                pass

            
class SignUpUserSerializer(serializers.ModelSerializer):
    """ Authentication SignUp Serializer """
    
    class Meta:
        model = models.User
        fields = (
            'id', 'email', 'username', 'password', 
        )
        read_only_fields = ('id', )
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'write_only': True}
        }
    
    def validate(self, data):
        validate_password(password=data['password'], user=models.User)
        return data
        
    def create(self, validated_data):
        if 'email' in validated_data and 'username' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
            return super(SignUpUserSerializer, self).create(validated_data)
        else:
            raise serializers.ValidationError('Unable to create user without email or username')


class UserSerializer(serializers.ModelSerializer):
    """ Default User Serializer """
    
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = models.User
        fields = '__all__'