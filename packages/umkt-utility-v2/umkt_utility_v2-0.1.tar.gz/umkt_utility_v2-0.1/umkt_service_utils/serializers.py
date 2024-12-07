from rest_framework import serializers
from django.contrib.auth.models import User, Group

class GroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name']

class UserSerializers(serializers.ModelSerializer):
    groups = GroupSerializers(many=True, read_only=True)

    class Meta:
        model = User
        # fields = '__all__'
        fields = ['username','first_name','last_name','email','is_superuser','is_staff','is_active','groups']