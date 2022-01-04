from rest_framework import serializers
from rest_framework.serializers import HyperlinkedIdentityField
from rest_framework.authtoken.models import Token

from .models import *
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password




class TaskSerializer(serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='api-taskdetail',
        format='html')

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta: 
    
        model = Task
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    tasks =  HyperlinkedIdentityField(many=True,
        view_name='api-taskdetail',
        read_only=True)


    class Meta:
        model = User
        fields = ['username', 'first_name',
    'last_name', 'email', 'tasks']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
 
        extra_kwargs = {'password': {
            'write_only':True,
            'required':True
        }}
 
 
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        
        return user