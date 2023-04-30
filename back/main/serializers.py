from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import CreditCard, MainUser
from .services import create_token


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    email = serializers.CharField(required=False)

    class Meta:
        model = MainUser
        fields = ('first_name', 'last_name', 'phone', 'email')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['token'] = create_token(instance, self.context['request'])
        return data


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ('first_name', 'last_name', 'phone', 'email', 'password')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = '__all__'


class MainUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return MainUser.objects.create(**validated_data)

    def to_representation(self, instance):
        data = super(MainUserSerializer, self).to_representation(instance)
        data['password'] = ""
        return data
