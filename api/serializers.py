from rest_framework import serializers
from rest_framework.serializers import HyperlinkedIdentityField
from django.contrib.auth.models import User
from .models import *

class TaskSerializer(serializers.ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='api-taskdetail',
        lookup_field='pk')

    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta: 
    
        model = Task
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all())


    class Meta:
        model = User
        fields = ['id', 'username', 'tasks']
        