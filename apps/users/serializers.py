from django.utils.crypto import get_random_string
from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=255, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, max_length=255, allow_blank=False, allow_null=False)
    repeat_password = serializers.CharField(required=True, max_length=255, allow_blank=False, allow_null=False)
    first_name = serializers.CharField(required=True, max_length=255, allow_blank=False, allow_null=False)
    last_name = serializers.CharField(required=True, max_length=255, allow_blank=False, allow_null=False)
    id = serializers.ReadOnlyField()

    def save_user(self, validated_data):
        user = User(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()
        if user is not None:
            raise serializers.ValidationError({'detail': 'email is existing'})

        if attrs['password'] != attrs['repeat_password']:
            raise serializers.ValidationError({'detail': 'password not match.'})

        attrs['email'] = attrs['email'].lower()
        attrs.pop('repeat_password')

        return attrs

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'repeat_password', 'first_name', 'last_name')


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255, allow_blank=False, allow_null=False)

    def update(self, instance, validated_data):
        key = validated_data['password_reset_key']
        instance.password_reset_key = key
        return instance

    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()
        if user is None:
            raise serializers.ValidationError({'detail': "Couldn't find your email"})
        password_reset_key = get_random_string(length=32)
        attrs['password_reset_key'] = password_reset_key
        return attrs

    class Meta:
        model = User
        fields = ('email')


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, max_length=255, allow_blank=False, allow_null=False)
    repeat_password = serializers.CharField(required=True, max_length=255, allow_blank=False, allow_null=False)

    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()
        if user is not None:
            raise serializers.ValidationError({'detail': 'email is existing'})

        if attrs['password'] != attrs['repeat_password']:
            raise serializers.ValidationError({'detail': 'password not match.'})

        attrs['email'] = attrs['email'].lower()
        attrs.pop('repeat_password')

        return attrs
