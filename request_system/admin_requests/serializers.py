from rest_framework import serializers
from .models import AdminRequest

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth import authenticate


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        # Return the user data if needed
        # You can customize this part to return additional user data
        data['user'] = user
        return data


#Serializer to Get User Details using Django Token Authentication
# class UserSerializer(serializers.ModelSerializer):
#     company = serializers.CharField(source='userprofile.company')
#     country = serializers.CharField(source='userprofile.country')

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'first_name', 'last_name', 'company', 'country')


    #Serializer to Register User

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import  CustomUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    # company = serializers.CharField(write_only=True, required=True)
    # country = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=CustomUser.ROLES, default='student')
    

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'role')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        # Extract company and country from validated_data
        # company = validated_data.pop('company')
        # country = validated_data.pop('country')
        # role = validated_data.pop('role')
        
        # Create the user instance
        user = CustomUser.objects.create_user(**validated_data)
        
        # # Create the UserProfile instance using company and country
        # UserProfile.objects.create(user=user, company=company, country=country, role=role)
        
        return user

    # This is the "to_representation" method to customize the output format when the instance is serialized.
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # rep['company'] = instance.userprofile.company
        # rep['country'] = instance.userprofile.country
        return rep

class AdminRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminRequest
        fields = '__all__'
        
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    
