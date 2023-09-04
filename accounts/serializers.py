from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.core.exceptions import ValidationError
from collections import OrderedDict
from datetime import datetime

from accounts.models import CustomUser, ValorantAccount


# serializers for the accounts - custom user
class AccountSerializer(ModelSerializer):
    password = serializers.CharField(
        min_length=8,
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        min_length=8,
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'password2', 'first_name', 'last_name', 'avatar', 'email']

    def create(self, validated_data):
        if validated_data['password'] != validated_data['password2']:
            raise ValidationError({
                'password': "The two password fields didn't match"
            })
        validated_data.pop('password2')
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):

        validated_data.pop('password2')
        if validated_data['username'] != '':
            instance.username = validated_data['username']
        if validated_data['password'] != '':
            instance.set_password(validated_data['password'])
        if validated_data.get('email', '') != '':
            instance.email = validated_data['email']
        if validated_data.get('first_name', '') != '':
            instance.first_name = validated_data['first_name']
        if validated_data.get('last_name', '') != '':
            instance.last_name = validated_data['last_name']
        if validated_data.get('avatar', '') != '':
            instance.avatar = validated_data['avatar']
        instance.save()
        return instance


class ValorantSerializer(ModelSerializer):
    class Meta:
        model = ValorantAccount
        fields = '__all__'
        depth = 1
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        owner = representation['owner']
        representation['created_at'] = representation['created_at'][:10]
        representation['test'] = 'testing'
        representation['updated_at'] = representation['updated_at'][:10]
        representation['owner'] = OrderedDict([
            ('id', owner.get('id')),
            ('username', owner.get('username')),
            ('email', owner.get('email')),
            ('admin', owner.get('is_superuser')),
            ('avatar', owner.get('avatar'))
        ])

        return representation

    def create(self, validated_data):
        return super().create(validated_data | {"owner": self.context['request'].user})
