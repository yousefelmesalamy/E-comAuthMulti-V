from rest_framework import serializers
from .models import USER


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ['id', 'username', 'email', 'password', 'is_active', 'is_seller', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}, 'is_active': {'read_only': True},
                        'is_superuser': {'read_only': True}}


class UserSellerSerializer(UserSerializer):

    def create(self, validated_data):
        user = USER.objects.create_user(**validated_data)
        user.is_seller = True
        user.save()
        return user


class BuyerSerializer(UserSerializer):
    # make is_seller read only
    is_seller = serializers.BooleanField(read_only=True)

    # another way to make is_seller read only
    def update(self, instance, validated_data):
        validated_data.pop('is_seller')
        return super().update(instance, validated_data)

    # another way to make is_seller read only
    def validate_is_seller(self, value):
        if value:
            raise serializers.ValidationError("you can't change is_seller value")
        return value

    # another way to make is_seller read only
    def validate(self, attrs):
        if attrs.get('is_seller'):
            raise serializers.ValidationError("you can't change is_seller value")
        return attrs

    # another way to make is_seller read only
    def create(self, validated_data):
        validated_data.pop('is_seller')
        return super().create(validated_data)

    # another way to make is_seller read only
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('is_seller')
        return data

    is_seller = serializers.BooleanField(read_only=True)
    is_seller.required = False

    def create(self, validated_data):
        validated_data.pop('is_seller')
        user = USER.objects.create_user(**validated_data)
        user.is_seller = False
        user.save()
        return user
