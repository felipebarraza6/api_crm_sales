"""Users Serializers."""

#DRF
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from django.contrib.auth import password_validation, authenticate

#Models
from api.crm.models import User, SalesModule

#Serializers
from api.crm.serializers import RetrieveModuleSalesInRetrieveUser

#Python
import jwt
from datetime import timedelta



class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class UserListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'date_joined',
            'is_active',
            'modified'
        )

class UserUpdateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name'
        )

class RetrieveUserModelSerializer(serializers.ModelSerializer):
    
    sales_modules_active = serializers.SerializerMethodField('get_actives_sales_modules')
    sales_modules_finishied = serializers.SerializerMethodField('get_finished_sales_modules')

    def get_finished_sales_modules(self, user):
        qs = SalesModule.objects.filter(user=user, is_active=False)
        serializer = RetrieveModuleSalesInRetrieveUser(instance=qs, many=True)
        return serializer.data

    def get_actives_sales_modules(self, user):        
        qs = SalesModule.objects.filter(user=user, is_active=True)
        serializer = RetrieveModuleSalesInRetrieveUser(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'date_joined',
            'created',
            'modified',
            'sales_modules_active',
            'sales_modules_finishied'
        )
        

class UserLoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)
    
    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Credenciales Invalidas')
        self.context['user']=user
        return data

    def create(self,data):
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class UserCreateSerializer(serializers.Serializer):

    email = serializers.EmailField(
		validators=[UniqueValidator(queryset=User.objects.all())]
	)
    username = serializers.CharField(
		min_length=4,
		max_length=20,
		validators=[UniqueValidator(queryset=User.objects.all())]
	)
	# Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

	# Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self,data):
        """Verify password match."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Password don't match.")
        password_validation.validate_password(passwd)
        return data
        
    def create(self, data):
        """Handle user and profile creation."""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    password = serializers.CharField(min_length=8, max_length=64, required=True)
    password_confirmation = serializers.CharField(min_length=8, max_length=64, required=True)

    def validate(self, data):
        password = data['password']
        password_confirmation = data['password_confirmation']
        if password != password_confirmation:
            raise serializers.ValidationError('Las contraseñas no coinciden')
        password_validation.validate_password(password)
        return data